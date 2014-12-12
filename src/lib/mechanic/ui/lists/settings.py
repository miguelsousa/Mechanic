from vanilla import CheckBoxListCell

from mechanic.storage import Storage
from mechanic.extension import Extension
from mechanic.ui.lists.extension import ExtensionList
from mechanic.ui.formatters.version import VersionFormatter


class SettingsList(ExtensionList):
    """Return an ExtensionList for settings window."""

    __columns = [{"title": "Check", "key": "check_for_updates", "width": 40, "editable": True, "cell": CheckBoxListCell()},
                 {"title": "Extension", "key": "name", "width": 300, "editable": False},
                 {"title": "Version", "key": "local_version", "editable": False, "formatter": VersionFormatter.alloc().init()}]

    def __init__(self, posSize, **kwargs):
        kwargs['columnDescriptions'] = self.__columns
        kwargs['editCallback'] = self.save
        configured = [e for e in Extension.all() if e.is_configured]
        super(SettingsList, self).__init__(posSize, configured, **kwargs)

    def save(self, sender):
        ignore = Storage.get("ignore")
        for row in self.get():
            if not row["check_for_updates"]:
                ignore[row["name"]] = True
            elif row["name"] in ignore:
                del ignore[row["name"]]
        print ignore
        Storage.set('ignore', ignore)
