function checkLogin(){
	var name=document.getElementById("TxtUserName");
	var password=document.getElementById("TxtPassword");
	
	if(name.value.length<1){
		alert("�û�������Ϊ�գ�");
		name.focus();
		return false;
		}
	if(password.value.length<1){
		alert("���벻��Ϊ�գ�");
		password.focus();
		return false;
		}	
		return true;
}