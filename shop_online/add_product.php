<?php
session_start();
include("dbconnect.php");
extract($_REQUEST);
$msg="";

$uname=$_SESSION['uname'];
	 if(isset($btn))
	 {
                                                      
 $mq=mysqli_query($connect,"select max(id) from pr_product1");
	 $mr=mysqli_fetch_array($mq);
	 $id=$mr['max(id)']+1;
	 
	 $img1="F".$id.$_FILES['file1']['name'];
	 $img2="B".$id.$_FILES['file2']['name'];
	 		
			move_uploaded_file($_FILES['file1']['tmp_name'],"upload/".$img1);
			move_uploaded_file($_FILES['file2']['tmp_name'],"upload/".$img2);
			
	 $ins=mysqli_query($connect,"insert into pr_product1(id,shop,product,pcode,price,img1,img2) values($id,'$uname','$product','$pcode','$price','$img1','$img2')");

 		if($ins)
		{
		
			
			
	 ?>
	 <script>
//Using setTimeout to execute a function after 5 seconds.
setTimeout(function () {
////   //Redirect with JavaScript
   window.location.href= 'add_product.php?act=success';
}, 500);
</script>
<?php
}


}

if($act=="del")
{
mysqli_query($connect,"delete from pr_product1 where id=$did");
?>
<script language="javascript">
window.location.href="add_product.php";
</script>
<?php
}
?>
<!DOCTYPE html>
<html lang="en">
   <head>
      <!-- basic -->
      <meta charset="utf-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <!-- mobile metas -->
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta name="viewport" content="initial-scale=1, maximum-scale=1">
      <!-- site metas -->
      <title><?php include("title.php"); ?></title>
      <meta name="keywords" content="">
      <meta name="description" content="">
      <meta name="author" content="">
      <!-- bootstrap css -->
      <link rel="stylesheet" href="css/bootstrap.min.css">
      <!-- style css -->
      <link rel="stylesheet" href="css/style.css">
      <!-- Responsive-->
      <link rel="stylesheet" href="css/responsive.css">
      <!-- fevicon -->
      <link rel="icon" href="images/fevicon.png" type="image/gif" />
      <!-- Scrollbar Custom CSS -->
      <link rel="stylesheet" href="css/jquery.mCustomScrollbar.min.css">
      <!-- Tweaks for older IEs-->
      <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css">
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/fancybox/2.1.5/jquery.fancybox.min.css" media="screen">
      <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script><![endif]-->
   </head>
   <!-- body -->
<body class="main-layout">
      <!-- loader  -->
     
      <!-- end loader --> 
      <!-- header -->
      <header>
         <!-- header inner -->
         <div class="header">
            <div class="head_top">
               <div class="container">
                  <div class="row">
                    <div class="col-xl-6 col-lg-6 col-md-6 col-sm-12">
                       <div class="top-box">
                        <ul class="sociel_link">
                         <li> <a href="#"><i class="fa fa-facebook-f"></i></a></li>
                         <li> <a href="#"><i class="fa fa-twitter"></i></a></li>
                         <li> <a href="#"><i class="fa fa-instagram"></i></a></li>
                         <li> <a href="#"><i class="fa fa-linkedin"></i></a></li>
                     </ul>
                    </div>
                  </div>
                  <div class="col-xl-6 col-lg-6 col-md-6 col-sm-12">
                       <div class="top-box">
                        <p><?php include("title.php"); ?></p>
                    </div>
                  </div>
               </div>
            </div>
         </div>
         <div class="container">
            <div class="row">
               <div class="col-xl-3 col-lg-3 col-md-3 col-sm-3 col logo_section">
                  <div class="full">
                     <div class="center-desk">
                        <div class="logo"> <a href=""><img src="images/logo.jpg" alt="logo"/></a> </div>
                     </div>
                  </div>
               </div>
               <div class="col-xl-7 col-lg-7 col-md-9 col-sm-9">
                  <div class="menu-area">
                     <div class="limit-box">
                        <nav class="main-menu">
                           <ul class="menu-area-main">
                              <li> <a href="add_product.php">Home</a> </li>
                              <li class="mean-last"> <a href="logout.php">Logout</a> </li>
                               
                           </ul>
                        </nav>
                     </div>
                  </div>
               </div>
               <div class="col-xl-2 col-lg-2 col-md-2 col-sm-2">
                  <!--<li><a class="buy" href="login.php">Login</a></li>-->
               </div>
            </div>
         </div>
         <!-- end header inner --> 
      </header>
      <!-- end header -->
       <div class="brand_color">
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <div class="titlepage">
                        <h2>Product</h2>
                    </div>
                </div>
            </div>
        </div>

    </div>

<div class="row">
			<div class="col-lg-3">
				
				<!-- A grey horizontal navbar that becomes vertical on small screens -->
			</div>
			
			
			
            <div class="col-lg-6">
              <div class="card"><div class="cardbill">
                <div class="card-header d-flex align-items-center">
                 
                </div>
                <div class="card-block">
                <form name="form1" method="post" enctype="multipart/form-data">
		  <div class="row">
					 <label class="col-sm-2 form-control-label">Product</label>
                      <div class="col-sm-10">
                        <div class="form-group">
                          <input type="text" name="product" class="form-control" required />
                        </div>
                      </div>
           </div>
		   <div class="row">
					 <label class="col-sm-2 form-control-label">Product Code</label>
                      <div class="col-sm-10">
                        <div class="form-group">
                          <input type="text" name="pcode" class="form-control" required />
                        </div>
                      </div>
           </div>
          <div class="row">
					 <label class="col-sm-2 form-control-label">Price</label>
                      <div class="col-sm-10">
                        <div class="form-group">
                          <input type="text" name="price" class="form-control" required />
						 
                        </div>
                      </div>
           </div>
           <div class="line"></div>
		   <div class="row">
					 <label class="col-sm-2 form-control-label">Front Image</label>
                      <div class="col-sm-10">
                        <div class="form-group">
                          <input type="file" name="file1" class="form-control" />
						  
                        </div>
                      </div>
           </div>
		   <div class="row">
					 <label class="col-sm-2 form-control-label">Back Image</label>
                      <div class="col-sm-10">
                        <div class="form-group">
                          <input type="file" name="file2" class="form-control" />
						  
                        </div>
                      </div>
           </div>
		  
		    <div class="row">
						<label class="col-sm-2 form-control-label"></label>
                      <div class="col-sm-10">
					  
                        <div class="form-group">
                          <input type="submit" name="btn" placeholder="" class="btn btn-primary" value="Submit" onClick="return validate()">
                        </div>
                      </div>
           </div>
		   </form>
                </div>
              </div></div>
			</div>
</div>	

<p>&nbsp;</p>
<h3 align="center">Product Information</h3>
<?php
$q1=mysqli_query($connect,"select * from pr_product1 where shop='$uname'");
$n1=mysqli_num_rows($q1);
if($n1>0)
{
?>
<table width="90%" border="1" align="center">
  <tr>
    <th width="9%" class="alert-primary">Sno</th>
	 <th width="17%" class="alert-primary">Front Image</th>
	  <th width="17%" class="alert-primary">Back Image</th>
    <th width="17%" class="alert-primary">Product</th>
    <th width="20%" class="alert-primary">Code</th>
    <th width="12%" class="alert-primary">Price</th>
    <th width="21%" class="alert-primary">Action</th>
  </tr>
  <?php
  $i=0;
  while($r1=mysqli_fetch_array($q1))
  {
  $i++;
  ?>
  <tr>
    <td><?php echo $i; ?></td>
	<td><img src="upload/<?php echo $r1['img1']; ?>" width="80" height="80"></td>
	<td><img src="upload/<?php echo $r1['img2']; ?>" width="80" height="80"></td>
    <td><?php echo $r1['product']; ?></td>
    <td><?php echo $r1['pcode']; ?></td>
    <td><?php echo $r1['price']; ?></td>
    <td><a href="add_product.php?act=del&did=<?php echo $r1['id']; ?>">Delete</a> </td>
  </tr>
  <?php
  }
  ?>
</table>
<?php
}



?>
<p>&nbsp;</p>
<!-- CHOOSE  -->

      
<!-- end CHOOSE -->

      <!-- service --> 
      
      <!-- end service -->

      
      <!--  footer --> 
       <footr>
         <div class="footer">
            <div class="container">
               <div class="row">
                  <div class="col-md-6 offset-md-3">
                     <ul class="sociel">
                         <li> <a href="#"><i class="fa fa-facebook-f"></i></a></li>
                         <li> <a href="#"><i class="fa fa-twitter"></i></a></li>
                         <li> <a href="#"><i class="fa fa-instagram"></i></a></li>
                         <li> <a href="#"><i class="fa fa-instagram"></i></a></li>
                     </ul>
                  </div>
            </div>
            
            
         </div>
            <div class="copyright">
              
            </div>
         
      </div>
      </footr>
      <!-- end footer -->
      <!-- Javascript files--> 
      <script src="js/jquery.min.js"></script> 
      <script src="js/popper.min.js"></script> 
      <script src="js/bootstrap.bundle.min.js"></script> 
      <script src="js/jquery-3.0.0.min.js"></script> 
      <script src="js/plugin.js"></script> 
      <!-- sidebar --> 
      <script src="js/jquery.mCustomScrollbar.concat.min.js"></script> 
      <script src="js/custom.js"></script>
      <script src="https:cdnjs.cloudflare.com/ajax/libs/fancybox/2.1.5/jquery.fancybox.min.js"></script>
      <script>
         $(document).ready(function(){
         $(".fancybox").fancybox({
         openEffect: "none",
         closeEffect: "none"
         });
         
         $(".zoom").hover(function(){
         
         $(this).addClass('transition');
         }, function(){
         
         $(this).removeClass('transition');
         });
         });
         
      </script> 
</body>
</html>