<?php
// === CONFIGURATION ===
$uploads_dir = 'uploads';         // Folder to store the image
$filename = 'current.jpg';        // Always overwrite this file
$password = '';         // Optional: set to '' to disable

// === SETUP ===
if (!is_dir($uploads_dir)) mkdir($uploads_dir, 0777, true);

$message = '';

// === PASSWORD PROTECTION ===
if ($password) {
    if (!isset($_POST['pass']) || $_POST['pass'] !== $password) {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $message = 'Incorrect password!';
        }
        // Show password form
        echo '<!DOCTYPE html><html><body>';
        if($message) echo "<p>$message</p>";
        echo '<form method="post">
                Password: <input type="password" name="pass" required>
                <button type="submit">Submit</button>
              </form></body></html>';
        exit;
    }
}

// === HANDLE UPLOAD ===
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $file = $_FILES['file'];
    $ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    $allowed = ['jpg','jpeg','png','webp'];

    if (!in_array($ext, $allowed)) {
        $message = 'Only JPG, JPEG, PNG, WEBP allowed.';
    } elseif (move_uploaded_file($file['tmp_name'], "$uploads_dir/$filename")) {
        $message = 'Upload successful!';
    } else {
        $message = 'Error uploading file.';
    }
}

// === HTML FORM ===
?>
<!DOCTYPE html>
<html>
<head>
    <title>Awww Uploader</title>
</head>
<body>
<h2>Upload Wallpaper</h2>
<?php if($message) echo "<p>$message</p>"; ?>
<form method="post" enctype="multipart/form-data">
    <?php if($password) echo '<input type="hidden" name="pass" value="'.htmlspecialchars($password).'">'; ?>
    <input type="file" name="file" required>
    <button type="submit">Upload</button>
</form>
<p>Current image: <a href="<?php echo $uploads_dir.'/'.$filename; ?>" target="_blank">View</a></p>
</body>
</html>
