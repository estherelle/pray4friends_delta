# Pray 4 Friends

Use this script to generate messages you can send to members of a small group so that they can pray for each other!

## Instructions

1. Add the names of your people and their gender to `prayers_inputs.txt`.
1. Add instructions on how they can find the other person's prayer in `pray4friend.py` by setting the `PRAYER_LOCATION` variable.
1. Run the script using `python pray4friends.py`.

## Features

1. The script automatically adds historical prayer data under the `prayer-history/` folder. This is so that people aren't praying for the same people too often.
1. The script outputs the results to `prayers_output.md`.

## Examples

After you provide an input like this:

```
John Doe,M
Brad Pitt,M
Jason Smith,M
George Washington,M
Ann Green,F
Holly Hills,F
Miranda Ellis,F
Tiffany Lee,F
Christian Smith,F
Annabelle Hero,F
Mille Mary,F
Natalie Young,F
```

You'll get an output for all the members of your small group like this in `prayers_output.md`:

```markdown
### Send this message to Joe Smith:

Hey, Joe! Hope you've been having a great week 🙂 Could you please pray for Johnny Cash at least once this week?

Please tell them you are praying for them!

You can find their prayer here:
https://bible.com

Thank you for praying for your brothers and sisters! 🙂
```

## Appendix

God bless you!