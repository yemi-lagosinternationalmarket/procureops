from frappe import _


def get_data():
	return [
		{
			"module_name": "LIM Procurement",
			"category": "Modules",
			"label": _("LIM Procurement"),
			"color": "grey",
			"icon": "octicon octicon-package",
			"type": "module",
			"description": "LIM-specific extensions to ERPNext.",
		}
	]
