# Format inspired from https://desktop.github.com/release-notes/
# Uses arium for html doc generation: https://pypi.org/project/airium/0.2.5/
#   pip install airium==0.2.5

# https://realpython.com/python-print/

import datetime
from github import Github
from pprint import pprint
from airium import Airium

def print_issue(a, issue, issueType):
  """
  :param a: airium object
  :param issue: issue object
  :param issuType: string {Added,  }
  """
  with a.div(klass='row Issue-Row'):
    with a.div(klass='col-1'):
      a(' ')
    with a.div(klass='col-1 text-center Issue-Type Issue-Type-' + issueType):
      a(issueType)
    with a.div(klass='col-10 Issue-Title'):
      a(issue.title + ' - ')
      with a.a(href='https://github.com/MikeH-Jac/AppCOM/issues/' + str(issue.number)):
        a('#' + str(issue.number))


# Doesn't work.
#g = Github("MikeH-Jac", "OWLMm326Wv5GUwbbO9xt")
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
g = Github("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")

repo = g.get_repo("Mikeh-Jac/AppCOM")

closed_milestones = repo.get_milestones(state='closed', sort='title', direction='desc')

#
# Airium
# Note that class is reserved in python, so klass is used instead.
#

a = Airium()

a('<!DOCTYPE html>')
with a.html(lang="en"):
  with a.head():
    a.meta(charset="utf-8")
    a.meta(name="viewport", content="width=device-width, initial-scale=1")
#    a.link(href="https://unpkg.com/@primer/css@^20.2.4/dist/primer.css", rel="stylesheet")
    a.link(href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css", rel="stylesheet", integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD", crossorigin="anonymous")
    a.link(rel="stylesheet", type="text/css", href="release-notes.css")
    a.title(_t="AppCOM Release Notes")

  with a.body():
    with a.h3(klass='main_header'):
      a("AppCOM Release Notes")
    # Iterate each closed milestone.
    for milestone in closed_milestones:
      release = repo.get_release(milestone.title)
      closed_issues = repo.get_issues(milestone, state='closed', sort='title')
      issues_new = []    # List of enhancement issues for the current milestone.
      issues_mod = []
      issues_fix = []
      issues_general = [] # General comments, not a specific issue type.
      for issue in closed_issues:
        for label in issue.labels:
      # if (label.color == '0052cc'):
      #   print('Module=', label)
      # else:
          if (label.name == 'bug'):
            issues_fix.append(issue)
          else:
            if (label.name == 'enhancement'):
              issues_new.append(issue)
            else:
              if (label.name == 'mod'):
                issues_mod.append(issue)
      # https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
      issues_new.sort(key=lambda x: x.title)
      issues_fix.sort(key=lambda x: x.title)
      issues_mod.sort(key=lambda x: x.title)

      with a.div(klass="container w-50 Milestone-Container"):
        with a.div(klass='row'):
          with a.div(klass='col-1 text-center Milestone-Title'):
            a(milestone.title)
          with a.div(klass='col-2 Milestone-Date'):
            d = release.published_at
            a(d.strftime('%b %d, %Y'))
          with a.div(klass='col-9'):
            a(' ')
        with a.div(klass='row'):
          with a.div(klass='col-1'):
            a(' ')
          descrLines = milestone.description.splitlines()
          with a.div(klass='col-11 Milestone-Description'):
            for l in descrLines:
              a(l +'<br>')
        for issue in issues_new:
          print_issue(a, issue, 'Added')
        for issue in issues_fix:
          print_issue(a, issue, 'Fixed')
        for issue in issues_mod:
          print_issue(a, issue, 'Changed')

# html = str(a)  # casting to string extracts the value
# print(html)
# or directly to UTF-8 encoded bytes:
html_bytes = bytes(a)  # casting to bytes is a shortcut to str(a).encode('utf-8')

# with open(r'mikeh-jac.github.io/appcom-release-notes.html', 'wb') as f:
with open(r'appcom-release-notes.html', 'wb') as f:
  f.write(html_bytes)


