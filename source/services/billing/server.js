'use strict'
const express = require('express')
const morgan = require('morgan')
const app = express()
const pkg = require('./package.json')
const AWS = require('aws-sdk')

let config

let s3 = new AWS.S3()
let params = {
  Bucket: "aws-linux-ops-configs",
  Key: "services/billing/config.json"
}

s3.getObject(params, function(err, data) {
  if (err) {
    console.log(err, err.stack) // an error occurred
    process.exit(1)
  }

  config = JSON.parse(data.Body)
  // console.log(config)
  run()
});

function run () {
  // use morgan to log all request in the Apache combined format to STDOUT
  app.use(morgan('combined'))

  // respond to all GET requests
  app.get('*', function (req, res) {
    res.set('Server', 'services/billing-v' + pkg.version)
    res.json({ message: 'billing service online', version: pkg.version });
  })

  app.listen(3000, function () {
    console.log('billing service listening on port 3000')
  })
}
