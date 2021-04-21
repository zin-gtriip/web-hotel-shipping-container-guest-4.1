var measurementID = JSON.parse(document.getElementById('ga-measurement-id').text || '""')

window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', measurementID);

function gaTag(action, category, label='', value='') {
    // example:
    // gtag('event', 'login', {
    //     'event_category': 'registration',
    //     'event_label': 'method',
    //     'value': 'Google'
    // });

    gtag('event', action, {
        'event_category': category,
        'event_label': label,
        'value': value
    });
}
