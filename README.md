## Howdy!

This is the project page for Flipreps (FLIght Plan REceipt Printing System)

# What it do?

If you go to skyvector.com, make a log (filling in your TAS, CRZ alt and ETD), render a PDF of it, then select all using Ctrl+A and paste it here, it will (using regex and basic math) create a JSON of that nav log, which then will be printed in a receipt printer.

You can also just copy something else (such as a lesson plan, checklists, etc...)

# Is this allowed?

I understand the world of general aviation, whilst not as regulated as commercial, is still pretty standardized. I never just take my receipt printed nav log with me -- I _always_ have my actual nav log copy with me. But since I have extra space on the plane for a receipt printed document... extra info never hurt anyone!

# Any bugs?

Probably a few here and there that I shall iron out in brief momments. The thing I struggled the most with was splitting the PDF for JSON, so any issue is probably coming from there.

Also,

- a custom GPS coord point in skyvector.com in the PDF is called UserFix
- this script will ask you to replace that with a name that makes sense to print (Village A, Ring Road on river B, ...)
- sometimes the array that populates the "UserFix"->custom name is a bit weird, and the last nav log item comes out as "UserFix" even if you wrote something down... haven't been able to pin point exactly what it is
- if you want to test before hand, just:
  - in the script.py uncomment the 2 "DEBUGGING?" comments towards the end of the file so you get some nice verbose
  - copy your navlog and when prompted type in the custom waypoints as 1, 2, 3, 4...
  - just make sure that the numbers make sense and are all there

# Feedback? Hate? Coffee?

me(at)carloslagoa.com

Thanks!
