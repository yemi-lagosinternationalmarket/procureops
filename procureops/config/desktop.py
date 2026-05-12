from frappe import _


def get_data():
	return [
		{
			"module_name": "ProcureOps",
			"category": "Modules",
			"label": _("ProcureOps"),
			"color": "grey",
			"icon": "octicon octicon-package",
			"type": "module",
			"description": "LIM-specific extensions to ERPNext.",
		}
	]
