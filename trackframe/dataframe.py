from __future__ import annotations
from typing import Any, Iterable, overload

import pandas as pd
from pandas.core.indexing import _LocIndexer, _iLocIndexer


class LocIndexer(_LocIndexer):
    """Loc indexer extended with variable usage and modification tracking."""

    def __init__(self, name: str, df: DataFrame):
        super().__init__(name, df)
        self._df = df

    def __setitem__(self, key: Any, value: Any):
        _, var = key
        self._df._register_modification(var)
        super().__setitem__(key, value)


class iLocIndexer(_iLocIndexer):
    """iLoc indexer extended with variable usage and modification tracking."""

    def __init__(self, name: str, ds: DataFrame):
        super().__init__(name, ds)
        self._df = ds

    def __setitem__(self, key: Any, value: Any):
        self._df._register_modification(self._df.columns)
        super().__setitem__(key, value)


class DataFrame(pd.DataFrame):
    """Modification-tracking version of pandas.DataFrame. The names of newly added or
    modified columns are stored in the `modified` attribute."""

    def __init__(self, *args, **kwargs):
        new = kwargs.pop("new", False)
        super().__init__(*args, **kwargs)

        self._metadata = {"modified": self.columns.to_list() if new else []}

    def _register_modification(self, key: str | Iterable[str]):
        """Register the modification of a variable or a set of variables."""
        if isinstance(key, str):
            key = [key]

        self.modified.extend(k for k in key if k not in self.modified)

    @overload
    def __setitem__(self, key: str, value: pd.Series): ...
    @overload
    def __setitem__(self, key: Iterable[str], value: pd.DataFrame): ...

    def __setitem__(self, key: str | Iterable[str], value: pd.Series | pd.DataFrame):
        self._register_modification(key)
        super().__setitem__(key, value)

    @property
    def loc(self) -> LocIndexer:
        return LocIndexer("loc", self)

    @property
    def iloc(self) -> iLocIndexer:
        return iLocIndexer("iloc", self)

    @property
    def metadata(self) -> dict[str, Any]:
        return self._metadata

    @property
    def modified(self) -> list[str]:
        """Names of all newly added or updated variables."""
        return self._metadata["modified"]