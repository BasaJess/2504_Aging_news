### "Modular"

The App has been desgined in a modular way to be able to switch pieces as it grows in the easiest posible way.

As of May/05/2025 it is composed of three major modules

1. Public Database retrieval of Documents
2. Creation and saving of Vector Database
3. Summarization and extraction of Information and publication in the Internet

Now in detail each of these sections:

# 1. Actualize the Documents database
To update the first point, there are at least two cases
1. Add a new public database to the poll already existing.
    - That means to create a new API connection to a new database and upload docs in full text pdf or XML
2. Upload new documents in the existing Pool.
    - That means to retrieve new docs since the last time 

# 2. Update the Vector DB
In this case we need to be sure that the update considers the already existing vecor_db for each file and it does not overwrite them to avoid extra time and computing time
This update will save a dataframe with all the necessary information that needs to be uploaded manually to GitHub

# 3. Publication
This seems to be the easiest since seems that nothing needs to be done, as the new df will be uploaded in the previous point
However as this is the UI, here we have room to modify, and expand the end functionality. Including the use and communication between two LLMs, one of them can use a database as a tool or memory, the question will be which db. It makes sense to use the complete vectordb and not the top_docs df list


As a reminder of how the App actually works, there is a [document](../00_Initiation_and_planning/How%20this%20App%20works.md) and an [image](../../images/Pipeline.png) 