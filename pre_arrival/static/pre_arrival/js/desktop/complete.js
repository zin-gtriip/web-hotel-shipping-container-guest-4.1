$('#btn-ok').click(function() {
    try { nextPage.postMessage('registrationDone'); } catch(error) {} // send message to app
});
