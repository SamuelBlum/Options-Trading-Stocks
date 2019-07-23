const {app, BrowserWindow} = require('electron') // http://electronjs.org/docs/api
const path = require('path') // https://nodejs.org/api/path.html
const url = require('url') // https://nodejs.org/api/url.html
const exec = require('child_process').exec;


let window = null

// Wait until the app is ready

app.once('ready', () => {

  webScrape();
  // Create a new window

  window = new BrowserWindow({
    // Set the initial width to 400px
    width: 400,
    // Set the initial height to 500px
    height: 500,
    // Don't show the window until it ready, this prevents any white flickering
    show: false,
    // allow the window to be resized.
    resizable: true
  })

  // Load a URL in the window to the local index.html path
  window.loadURL(url.format({
pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }))

  // Show window when page is ready
window.once('ready-to-show', () => {
 window.show()
})
})

function webScrape () {
    exec('../pynance.py');   
 //    var python = require('child_process').spawn('python',['./scottrade.py']);
}
