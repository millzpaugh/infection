# infection

This project outlines the following challenge: 

When rolling out big new features, sites like to enable them slowly, starting with just a team, then a handful of users, then some more users, and so on, until all users have the feature. This insulates the majority of users from bad bugs that crop up early in the life of a feature.

Ideally every user in any given classroom to be using the same version of the site. Enter “infections”. We can use the heuristic that each teacher-student pair should be on the same version of the site. So if A coaches B and we want to give A a new feature, then B should also get the new feature. Note that infections are transitive - if B coaches C, then C should get the new feature as well. Also, infections are transferred by both the “coaches” and “is coached by” relations.

First, model users (one attribute of a user is the version of the site they see) and the coaching relations between them. A user can coach any number of other users. You don’t need to worry about handling self-coaching relationships.

Now implement the infection algorithm. Starting from any given user, the entire connected component of the coaching graph containing that user should become infected.


This Django project is a visualization of the challenge described above, available here: https://warm-spire-20456.herokuapp.com
