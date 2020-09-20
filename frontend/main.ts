function generateURL()
{
  let inputElement = document.getElementById('longURL') as HTMLInputElement;
  let longUrl = inputElement.value;
  makeHttpRequest(longUrl, (message: string) => { alert(message) });
}
  
async function makeHttpRequest(targetURL: string, onSuccess: Function) 
{
  let myUrl = `https://xj0sreihya.execute-api.us-west-2.amazonaws.com/prod/?targetURL=${targetURL}`;

  const response = await fetch(myUrl, {
    method: 'GET',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
   });
  
  if (!response.ok) { /* Handle */ }
  
  // If you care about a response:
  if (response.body !== null) {
    // body is ReadableStream<Uint8Array>
    // parse as needed, e.g. reading directly, or
    //const asString = new TextDecoder("utf-8").decode(response.body);
    // and further:
    //const asJSON = JSON.parse(asString);  // implicitly 'any', make sure to verify type on runtime.
  }
}