const { text } = require('micro')
const { parse } = require('querystring')
const { appendFoo } = require('./lib/eval')


module.exports = (req, res) => {
  // Parse code received through req
  // console.log(req)
  // const { body } = req;
  // let result, attachments

  // try {
  //   console.log(body)
  //   result = appendFoo(body.text)

  // } catch (error) {

  //   result = error.message
  //   attachments = [{ text: error.stack }]

  // }

  // const response_type = 'in_channel'

  res.writeHead(200, { 'Content-Type': 'application/json' })
  // Create response object and send result back to Slack
  res.send("hello")
}