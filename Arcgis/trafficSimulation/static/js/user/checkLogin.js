function checkLogin(){
	var name=document.getElementById("TxtUserName");
	var password=document.getElementById("TxtPassword");
	
	if(name.value.length<1){
		alert("用户名不能为空！");
		name.focus();
		return false;
		}
	if(password.value.length<1){
		alert("密码不能为空！");
		password.focus();
		return false;
		}	
		return true;
}