![CNCA logo](http://www.cenat.ac.cr/templates/shaper_mybiz/images/styles/style1/cnca_top.gif)

# Torquitor

## Synopsis

`Torquitor` is a simple yet effective web interface for Adaptative Computing's Torque. It uses a python daemon to obtain load data from pbsnodes and qstat and displays the information in a web interface through a php service.

## Motivation

The pbsnodes and qstat tools display very useful information, yet their console display is not quick or comfortable to use, the alternative web interface, provided by `Torquitor` shows information from every node, and every running job in a clear, easy to the eye, web interface available for every user of the cluster.

## Installation

Copy the package and run `install.sh`, follow the steps in the process. 
Torquitor requires `pbsnodes`, `qstat`, `python 2.7`, `apache` or `nginx` and `php 5.x` already installed in the server, it also requires `superuser` permissions to run properly.

## Contributors

Contact `cnca@cenat.ac.cr` if you want to contribute to the project.

## License

CC-BY-SA
