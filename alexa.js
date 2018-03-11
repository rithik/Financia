var http = require('http');
var prod_url = "http://502310d3.ngrok.io";

exports.handler = (event, context) => {

    try {

        if (event.session.new) {
            // New Session
            console.log("NEW SESSION");
        }

        switch (event.request.type) {

            case "LaunchRequest":
                // Launch Request
                console.log(`LAUNCH REQUEST`)
                break;
            case "IntentRequest":
                switch (event.request.intent.name) {
                    case "gainMoney":
                        var dollars = event.request.intent.slots.dollars.value;
                        var responseA = ["Good job earning money!", "Earnings recorded", "Okay", "Keep it up"];
                        var url = prod_url + "/alexa/income/" + dollars;
                        console.log("its lit")
                        http.get(url, function(res) {
                        context.succeed(generateResponse(buildSpeechletResponse(responseA[Math.floor(Math.random() * 4)], true)))
                         }).on('error', function(e) {
                            console.log("Got error: " + e.message);
                            context.done(null, 'FAILURE');
                             });
                        break;
                    case "gainMoneyCents":
                        var dollars = event.request.intent.slots.dollars.value;
                        var cents = event.request.intent.slots.cents.value;
                        var response = "Good job earning money!";
                        var url = prod_url + "/alexa/income/" + dollars +"." + cents;
                        http.get(url, function(res) {
                        context.succeed(generateResponse(buildSpeechletResponse(responseA[Math.floor(Math.random() * 4)], true)))
                         })
                        break;
                    case "looseMoney":
                        var dollars = event.request.intent.slots.dollars.value;
                        var responseA = ["Make sure you watch your spending", "Transaction Recorded", "Okay", "Okay, make sure to keep me up to date"];
                        var url = prod_url + "/alexa/expense/" + dollars + "/" + "Other";
                        http.get(url, function(res) {
                        context.succeed(generateResponse(buildSpeechletResponse(responseA[Math.floor(Math.random() * 4)], true)))
                         })
                        break;
                    case "looseMoneyCents":
                        var dollars = event.request.intent.slots.dollars.value;
                        var cents = event.request.intent.slots.cents.value;
                        var responseA = ["Make sure you watch your spending", "Transaction Recorded", "Okay", "Okay, make sure to keep me up to date"];
                        var url = prod_url + "/alexa/expense/" + dollars + "."+ cents + "/" + "Other";
                        http.get(url, function(res) {
                        context.succeed(generateResponse(buildSpeechletResponse(responseA[Math.floor(Math.random() * 4)], true)))
                         })
                        break;
                    case "looseMoneyCat":
                        var dollars = event.request.intent.slots.dollars.value;
                        var cat = event.request.intent.slots.category.value;
                        var responseA = ["Make sure you watch your spending", "Transaction Recorded", "Okay", "Okay, make sure to keep me up to date"];
                        var url = prod_url + "/alexa/expense/" + dollars + "/" + cat.substring(0,1).toUpperCase() + cat.substring(1);
                        http.get(url, function(res) {
                        context.succeed(generateResponse(buildSpeechletResponse(responseA[Math.floor(Math.random() * 4)], true)))
                         })
                        break;
                    case "looseMoneyCatCents":
                        var dollars = event.request.intent.slots.dollars.value;
                        var cents = event.request.intent.slots.cents.value;
                        var cat = event.request.intent.slots.category.value;
                        var responseA = ["Make sure you watch your spending", "Transaction Recorded", "Okay", "Okay, make sure to keep me up to date"];
                        var url = prod_url + "/alexa/expense/" + dollars + "." + cents + "/" + cat.substring(0,1).toUpperCase() + cat.substring(1);
                        http.get(url, function(res) {
                        context.succeed(generateResponse(buildSpeechletResponse(responseA[Math.floor(Math.random() * 4)], true)))
                         })
                        break;
                    case "investStock":
                        var numOfStock =  event.request.intent.slots.numOfShares.value;
                        var nameOfStock = event.request.intent.slots.nameOfStock.value;
                        var response = "invest stock " + numOfStock + " shares " + nameOfStock;
                        context.succeed(generateResponse(buildSpeechletResponse(response, true)))
                        break;
                    case "investCrypto":
                        var dollars = event.request.intent.slots.dollars.value;
                        var nameOfCrypto = event.request.intent.slots.nameOfCrypto.value;
                        var response = "invest crypto " + dollars + " " + nameOfCrypto;
                        context.succeed(generateResponse(buildSpeechletResponse(response, true)))
                        break;
                    case "transferMoney":
                        var dollars = event.request.intent.slots.dollars.value;
                        var userID = event.request.intent.slots.userID.value;
                        var response = "transfer " + dollars + " to " + userID;
                        context.succeed(generateResponse(buildSpeechletResponse(response, true)))
                        break;
                    case "transferMoneyCents":
                        var dollars = event.request.intent.slots.dollars.value;
                        var cents = event.request.intent.slots.cents.value;
                        var userID = event.request.intent.slots.userID.value;
                        var response = "transfer " + dollars + " and " + cents + " to " + userID;
                        context.succeed(generateResponse(buildSpeechletResponse(response, true)))
                        break;
                    default:
                        throw "Invalid intent"
                }
                break;
            case "SessionEndedRequest":
                console.log(`SESSION ENDED REQUEST`)
                break;
            default:
                context.fail(`INVALID REQUEST TYPE: ${event.request.type}`);

        }

    } catch (error) {
        context.fail(`Exception: ${error}`)
    }

}

// Helpers
buildSpeechletResponse = (outputText, shouldEndSession) => {

    return {
        outputSpeech: {
            type: "PlainText",
            text: outputText
        },
        shouldEndSession: shouldEndSession
    }

}

generateResponse = (speechletResponse, sessionAttributes) => {

    return {
        version: "1.0",
        sessionAttributes: sessionAttributes,
        response: speechletResponse
    }

}