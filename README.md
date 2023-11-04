# Pray 4 Friends

Use this script to generate messages you can send to members of a small group so that they can pray for each other!

## Instructions

1. Run the generation script `./starter_files.py`. Get the `prayers_input.md` and `constants.py` starter files.
    1. Add the names of your people and their gender to `prayers_input.md`.
    1. Add instructions on how they can find the other person's prayer:
        1. Set the `PRAYER_LOCATION` variable in `constants.py`. This will be a link to a Google Doc with the prayers.
1. Run the script using `./lib/generate_prayers.py`.

## Features

1. The script automatically adds historical prayer data under the `prayer-history/` folder. This is so that people aren't praying for the same people too often.
1. The script outputs the results to `prayers_output.md`.

## Examples

After you provide an input like this:

```markdown
## M
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

You will also get a file automatically generated in `prayer-history/202X-XX-XX.md`. Commit that file and make a pull request on the repo.

```bash
$ git add .
$ git commit -m "202X-XX-XX prayer history"
$ git push
```

Go to the [Delta GitHub Repo](https://github.com/estherelle/pray4friends_delta) and create a pull request.

## Appendix

God bless you!
