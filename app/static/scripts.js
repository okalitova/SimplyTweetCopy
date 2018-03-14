function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
    });
};
function onLoad() {
    gapi.load('auth2', function() {
        gapi.auth2.init();
    });
};
function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    console.log("ID: " + profile.getId());
    console.log("Full Name: " + profile.getName());
    console.log("Given Name: " + profile.getGivenName());
    console.log("Family Name: " + profile.getFamilyName());
    console.log("Image URL: " + profile.getImageUrl());
    console.log("Email: " + profile.getEmail());

    var id_token = googleUser.getAuthResponse().id_token;
    console.log("ID Token: " + id_token);
    
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) { // when completed we can move away
            console.log("Redirected to the main page");
            window.location = "/";
        }
    }
    xhr.open('POST', '/accept_token');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        console.log('Signed in as: ' + xhr.responseText);
    };
    xhr.send('idtoken=' + id_token);
};

