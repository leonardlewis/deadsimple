function signupValidate() {
  var pass1 = document.getElementById("pass1").value;
  var pass2 = document.getElementById("pass2").value;
  if (pass1 != pass2) {
    alert("Passwords do not match.");
    document.getElementById("pass1").style.borderColor = '#E32434';
    document.getElementById("pass2").style.borderColor = '#E32424';
    return false;
  }
  else {
    return true;
  }
  }
