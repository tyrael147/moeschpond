# Make Moeschberg Even Greater

Repository of the development of the LCA analysis 

## Instructions the repo

A github account is required. The following instruction allow authentication and cloning:

```shell
cd
git clone https://<YOUR_USER_NAME>:<YOUR_TOKEN>@github.com/tyrael147/moeschpond.git
````
A user email and user name are required if you are using git for the first time:

```shell
git config --global user.name <"YOUR_USER_NAME">
git config --global user.email <"YOUR_EMAIL">
```
After a change has been done, you can make your first commit doing the following:
- Add all the files in the folder to be tracked:
```shell
git add . 
```
- Now commit the changes and push:
```shell
git commit -m "your commit message"
git push
```


## About the calculations

- `data_search.ipynb` is used to explore and obtain ids, names, and metada.
- `premise.ipynb` is used to generate different premise databases and export everything as a *.tar.gz file
- `premise importer.ipynb` is required to load the *.tar.gx (built in in bw2) and write it in disk. This is mandatory since bw5 cannot read and write bw2 projetcs from memory, only from disk
- `Wood pellets regionalized Nicolas.ipynb` contains the steps to regionalize background nodes without altering the original database
- `LCA_foreground.ipynb` shows the steps followed to generate the scenario analysis with premise.
