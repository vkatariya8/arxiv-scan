def add_tiddler_subtext(title, url):
	subtiddler_text = [None] * 5
	subtiddler_text[0] = "* [["
	subtiddler_text[0] += title
	subtiddler_text[0] += "|"
	subtiddler_text[0] += url
	subtiddler_text[0] += "]]"
	subtiddler_text[1] = "** "
	subtiddler_text[2] = "\"\"\""
	subtiddler_text[3] = "\"\"\""
	subtiddler_text[4] = ""
	return subtiddler_text