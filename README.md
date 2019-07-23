# PYNANCE APP

Simple [Electron](http://electronjs.org) application that shows undervalued options off the NASDAQ. Undervalued is defined for call options as being sold for less than it could be executed and sold for.

## Getting started

- Install [Node LTS](https://nodejs.org)
- Clone this repository
- `npm install` to install the application's dependencies
- `npm start` to start the application

## Architecture

- `pynance.py` is the backend webscraping script that searches scottrade for undervalued options. This script will be deployed to the cloud.
- `app` folder contains the front end of the app
- `aws_routines.py` will be the communication between the cloud instance of the backend, and the client

## Going further

Here are some ideas on how it can be improved using other Electron APIs.

- Double-click commodity to open directly
- Refresh automatically on an interval.
- Export prices to a `.csv` file.
- Show percentage change in price.
- Show notifications through SNS when prices go above/below certain amounts.
