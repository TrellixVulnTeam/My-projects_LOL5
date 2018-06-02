<?php
 header("Access-Control-Allow-Origin: *");

print_r("enteredddd");
print_r($_FILES);

if(is_array($_FILES)) {
if(is_uploaded_file($_FILES['fileToUpload']['tmp_name'])) {
$sourcePath = $_FILES['fileToUpload']['tmp_name'];
$targetPath = "uploads/".$_FILES['fileToUpload']['name'];
if(move_uploaded_file($sourcePath,$targetPath)) {
?>
<!--<img src="<?php echo $targetPath; ?>" width="200px" height="200px" class="upload-preview" /> -->
<?php
echo "success";
}else{
echo "Error on Uploding....";
}
}
else{
echo "NO Image selected";
}

}

?>

