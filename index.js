const { text } = require('micro')
const { parse } = require('querystring')
const { appendFoo } = require('./lib/eval')


module.exports = async (req, res) => {
  // Parse code received through req
  // const body = parse(await text(req))
  console.log(req)
  res.send("yo")

  // let result, attachments

  // try {
  // console.log(body)
  //   result = appendFoo(body.text)

  // } catch (error) {

  //   result = error.message
  //   attachments = [{ text: error.stack }]

  // }

  // const response_type = 'in_channel'

  // res.writeHead(200, { 'Content-Type': 'application/json' })

}