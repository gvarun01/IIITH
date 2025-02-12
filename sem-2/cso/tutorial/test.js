// const qs = require('querystring');
import axios from 'axios';
import qs from 'querystring';

// Define the prompt to be sent
const prompt = 'Please generate a simple blog post according to this title "What is CHATGPT"';

// Enter E-mail to generate API
const apiKey = 'ae96d80559ad8428a19fb072f3f908bb';

// Define the default model if none is specified
const defaultModel = 'gpt-3.5-turbo';

// Uncomment the model you want to use, and comment out the others
// const model = 'gpt-4';
// const model = 'gpt-4-32k';
// const model = 'gpt-3.5-turbo-0125';
const model = defaultModel;

// Build the URL to call
const apiUrl = `http://195.179.229.119/gpt/api.php?${qs.stringify({
  prompt: prompt,
  api_key: apiKey,
  model: model
})}`;

// Execute the HTTP request
axios.get(apiUrl)
  .then(response => {
    // Print the response data
    console.log(response.data);
  })
  .catch(error => {
    // Print any errors
    console.error('Request Error:', error.message);
  });