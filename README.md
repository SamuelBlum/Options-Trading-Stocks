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

## Finding Undervalued Call Options

A call option is considered undervalued when the ask price is less than the difference between the current stock price and the strike price. While this is rare, there are several reasons for this situation to occur.

- Margin calls
- Very low volume trading
- Option is set to expire with no one bidding

## Going further

Here are some ideas on how it can be improved using other Electron APIs.

- Double-click commodity to open directly
- Refresh automatically on an interval.
- Export prices to a `.csv` file.
- Show percentage change in price.
- Show notifications through SNS when prices go above/below certain amounts.
