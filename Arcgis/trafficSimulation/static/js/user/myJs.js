//检查是否为邮箱
function isEmail(field,alerttxt)
{
with (field)
{
apos=value.indexOf("@");
dotpos=value.lastIndexOf(".");
if (apos<1||dotpos-apos<3) 
  {alert(alerttxt);return false;}
else {return true;}
}
}
//检查是否为空
function isNull(field,alerttxt)
{
with (field)
  {
  if (value==null||value=="")
    {alert(alerttxt);return false;}
  else {return true;}
  }
}
//login check
function checkLogin(thisform)
{
	with (thisform)
	  {
	  if (isNull(account,"账户不能为空!请重新输入")==false)
	    {account.focus();return false;}
	  if (isNull(password,"密码不能为空!请重新输入")==false)
	    {password.focus();return false;}
	  }
}
//changePassword check
function isMatch(field1,field2,alertText)
{
		if(field1.value!=field2.value)
			{alert(alertText);return false;}
		else return true;
}
function checkPassword(thisform)
{
	with(thisform)
	{
		if (isNull(manPassword,"请输入旧密码!请重新输入")==false)
	    {manPassword.focus();return false;}
		if (isNull(newPassword1,"新密码不能为空!请重新输入")==false)
	    {newPassword1.focus();return false;}
	    if (isNull(newPassword2,"确认的新密码不能为空!请重新输入")==false)
	    {newPassword2.focus();return false;}
	    if(isMatch(newPassword1,newPassword2,"两次输入的密码不一致!请重新输入")==false)
	    {newPassword1.focus();newPassword2.focus();return false;}
	}
}
//appendAdmin check
function checkAppendAdmin(thisform)
{
	with (thisform)
	  {
	  if (isNull(manNo,"账号不能为空!请重新输入")==false)
	    {manNo.focus();return false;}
	  if(isEmail(manNo, "账号必须为新授权的管理员的邮箱!")==false)
		{manNo.focus();return false;}
	  if (isNull(manName,"姓名不能为空!请重新输入")==false)
	    {manName.focus();return false;}
	  }
}
//appendAnn check
function checkAppendAnn(thisform)
{
	with (thisform)
	  {
	  if (isNull(aTitle,"公告标题不能为空!请重新输入")==false)
	    {aTitle.focus();return false;}
	  if (isNull(aText,"公告内容不能为空!请重新输入")==false)
	    {aText.focus();return false;}
	  }
}