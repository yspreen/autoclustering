I have attached the files for adding in the clustering and analysis. I’ve also included a working of the UI.

For the python portion, you probably won’t need many of the functions, but they are there just in case. Call them as you’d like. The R script should generate the clusterings in the folder it is run from (./partitions/file_name) as long as an input file is passed in via command line args.

The UI is based on a React model. Basically, the data exists somewhere and is retrieved by the ‘Data’ class which is really just a controller for the view class, which is named as such. Anytime there is an update to the array of objects by the user (for example, attach a DOM listener for when a user clicks to add/remove a row from their selection) the state of the component is updated and React takes care of updating everything efficiently.

Hopefully everything looks good. If you have any questions of course feel free to ask!