app_name = "lim_procurement"
app_title = "LIM Procurement"
app_publisher = "Lagos International Market"
app_description = "LIM-specific extensions of ERPNext: Custom Fields, Custom DocTypes, hooks, and whitelisted REST methods. See https://github.com/yemi-lagosinternationalmarket/b2b-starter ADR 0018/0019."
app_email = "ibrahimolayemi09@gmail.com"
app_license = "Proprietary"

# Fixtures — versioned customizations exported as data, not patches.
# See ADR 0019: Custom Fields ride in fixtures, not in ERPNext source.
fixtures = [
	{"dt": "Custom Field", "filters": [["name", "like", "Supplier-%"]]},
]
