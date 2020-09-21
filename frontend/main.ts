function generateURL()
{
  let inputElement = document.getElementById('long-url') as HTMLInputElement;
  let longUrl = inputElement.value;
  makeHttpRequest(longUrl, (message: string) => { alert(message) });
}

function copyUrl()
{
  let inputElement = document.getElementById('long-url') as HTMLInputElement;
  let longUrl = inputElement.value;
  makeHttpRequest(longUrl, (message: string) => { alert(message) });
}
  
async function makeHttpRequest(targetURL: string, onSuccess: Function) 
{
  let myUrl = `https://xj0sreihya.execute-api.us-west-2.amazonaws.com/prod/?targetUrl=${targetURL}`;

  const response = await fetch(myUrl, {
    method: 'GET',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
   });
  
  if (!response.ok) { /* Handle */ }
  
  // If you care about a response:
  if (response.body !== null) {
    const asJson = await response.json();
    console.log(asJson);

    const urlResponse = Object.assign(new UrlResponse, asJson) as UrlResponse;
    console.log(urlResponse.Url);
    
    let resultContainer = document.getElementById('result-container') as HTMLInputElement;
    let resultInput = document.getElementById('long-url') as HTMLInputElement;
    resultInput.value = urlResponse.Url as string;
    resultContainer.style.display = 'block';
  }
}

class UrlResponse{
  public Url?: string;
}