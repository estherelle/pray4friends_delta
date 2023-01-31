#!/usr/bin/env python3

"""
Generates initial files for the pray4friends.py script to work.
"""

with open('prayers_input.md', 'w') as in_f:
    in_f.write("""## M
John Doe
Brad Pitt
Jason Smith
George Washington
## F
Ann Green
Holly Hills
Miranda Ellis
Tiffany Lee
Christian Smith
Annabelle Hero
Mille Mary
Natalie Young
""")

with open('constants.py', 'w') as in_f:
    in_f.write("""\"\"\"
Changes these values for your small group!
\"\"\"

PRAYER_LOCATION='https://bible.com'
""")
