var ip = '';
fetch('https://api.ipify.org/?format=json')
.then(function (response) 
{
    return response.json();
})
.then(function(data)
{
    ip = data.ip;

    fetch('/get_user_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ip: ip })
        });
});