#!/usr/bin/env python3

"""
Generates initial files for the pray4friends.py script to work.
"""

# Prayer Inputs
PRAYER_INPUTS = 'prayers_input.md'
with open(PRAYER_INPUTS, 'w') as in_f:
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

# Constants file
CONSTANTS = 'lib/constants.py'
with open(CONSTANTS, 'w') as in_f:
    in_f.write("""\"\"\"
Changes these values for your small group!
\"\"\"

PRAYER_LOCATION='https://bible.com'
""")
