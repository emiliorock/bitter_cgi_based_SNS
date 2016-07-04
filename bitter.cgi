#!/usr/bin/perl -w

#--------------------------------------------------#
#   This assignment was written by Huang Mengxin   #
#              Student ID z5013846                 #
#               The css links to                   #
#http://getbootstrap.com/dist/css/bootstrap.min.css#

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use DBI;
use POSIX;

$page = 0;
$k = 0;

sub main() {

    #connect to cse mysql server
    #the large dataset is already stored in the database

    $host = 'z5013846.srvr';
    $database = 'bitter';
    $dbh = DBI->connect("DBI:mysql:database=$database;host=$host;port=3306", "z5013846", "z5013846");

    # define some global variables
    $debug = 1;
    $dataset_size = "large"; 
    $users_dir = "dataset-$dataset_size/users";
    $bleats_dir = "dataset-$dataset_size/bleats";

    print page_header();
    warningsToBrowser(1);

    # print current time
    ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time);
    $mon += 1;
    $year += 1900;
    print "<span class='badge'>Current time: $mday/$mon/$year $hour:$min:$sec </span><p>";

    $current_url = $ENV{'SCRIPT_URI'};


    $login_div = param('login_div') || '';
    $search_div = param('search_div') || '';

    # if the user has received the confirmation email, 
    # then he will be automatically sent to confirm page via the url in the email 
    if (defined param('goto_confirm') && param('goto_confirm') eq '1') {
        $login_div = 1;
        $search_div = 1;
        print_confirm_page();
    }

    # if the user forget his password,
    # he will go to the forget password page
    if (defined param('Forget Password')) {
        $login_div = 1;
        $search_div = 1;
        forget_password();
    }

    # if the user wants to sign up
    if (defined param('goto_signup') && param('goto_signup') eq '1') {
        $login_div = 1;
        $search_div = 1;
        sign_up();
    }

    # if the user logs in
    if ($login_div eq '') {
        if (param('login_username') ne '' && param('login_password') ne '') {
            login_page();
        }
        else {
            print
            "<form method='POST' action=''>
            <legend>New to Bitter?</legend>
            <input type='submit' value='Sign Up Now' class='btn btn-success'>
            <input type='hidden' name='goto_signup' value='1'>
            </form><p>  
            <form method='POST' action=''>
            <legend>Already had an account</legend>
            <div class='input-group'>
                <input type='text' name='login_username' class='form-control' placeholder='Username (*)' aria-describedby='sizing-addon1'><p>
            </div><p>
            <div class='input-group'>
                <input type='password' name='login_password' class='form-control' placeholder='Password (*)' aria-describedby='sizing-addon1'><p>
            </div><p>
            <div class='input-group'>
            <input type='submit' value='Sign In' class='btn btn-success'>
            </div><p><div class='input-group'>
            <input type='submit' name='Forget Password' value='Forget Password' class='btn btn-success'>
            </div><p>
            </form>";        
        } 
    }

    $current_username = param('current_username') || '';
    $current_password = param('current_password') || '';

    # if the user wants to search for user or bleat
    if ($search_div eq '') {
        print 
        "<div class='row'>
        <div class='input-group'>
            <legend>Search</legend>
            <form method='POST'>
                <select name='search_by' class='selectpicker'>
                <option value='search_username'>Username</option>
                <option value='search_fullname'>Fullname</option>
                <option value='search_bleat'>Bleat</option>
                </select><p><p><p>
                <div class='input-group'><input type='text' name='search_content' class='form-control' placeholder='Search for...''></div><p>
                <div class='input-group'><input type='submit' value='Search' class='btn btn-success'></div>
                <input type='hidden' name='login_username' value='$current_username'>
                <input type='hidden' name='login_password' value='$current_password'>
                <input type='hidden' name='Search Page' value='Search Page'>
            </form><p>
        </div>
        </div>";
        if (defined param('search_content')) {
            if (param('search_content') ne '') {
                search_result();
                param('Search Page', 'Search Page');
            }
        }
    }

    if (!defined param('Search Page')) {
        user_page();
        bleat_page();
    }
    print page_trailer();

    $dbh->disconnect();
}

# send eamil function
sub send_mail {
    my ($tofield, $subject, $text, $fromfield) = @_;
    my $mailprog = "/usr/lib/sendmail";
    open my $ph, '|-', "$mailprog -t -oi" or die $!;
    print $ph "To: $tofield\n";
    print $ph "From: $fromfield\n";
    print $ph "Reply-To: $fromfield\n";
    print $ph "Subject: $subject\n";
    print $ph "\n";
    print $ph "$text";
    close $ph;
    return ;
}

# sign up function when the sign up page is called
sub sign_up {
    print <<eof;
    <div class=="container">
    <div class="row">
    <div class="col-md-6">     
        <legend>Sign Up Now</legend>
        <form method='POST' action='' enctype="multipart/form-data">
        <div class="input-group">
            <input type="text" name='sign_up_username' class="form-control" placeholder="Username (*)" aria-describedby="sizing-addon1"><p>
        </div><p><div class="input-group">    
            <input type="password" name='sign_up_password1' class="form-control" placeholder="Password (*)" aria-describedby="basic-addon1"><p>
        </div><p><div class="input-group">    
            <input type="password" name='sign_up_password2' class="form-control" placeholder="Confirm Password (*)" aria-describedby="basic-addon1"><p>
        </div><p><div class="input-group">
            <input type="text" name='sign_up_email' class="form-control" placeholder="Email (*)" aria-describedby="basic-addon1"><p>
        </div><p><div class="input-group">
            <input type="text" name='sign_up_fullname' class="form-control" placeholder="Fullname" aria-describedby="basic-addon1"><p>
        </div><p><div class="input-group">
            <input type="text" name='sign_up_suburb' class="form-control" placeholder="Home Suburb" aria-describedby="basic-addon1"><p>
        </div><p><div class="input-group">
            <input type="text" name='sign_up_latitude' class="form-control" placeholder="Home Latitude" aria-describedby="basic-addon1"><p>
        </div><p><div class="input-group">
            <input type="text" name='sign_up_longtitude' class="form-control" placeholder="Home Longitude" aria-describedby="basic-addon1"><p>
        </div><p><div class="input-group">
        Profile Image
        </div><p>
        <input type="file" name='sign_up_image' value='Upload' class='btn btn-default'>
        <p><div class="input-group">
        Do you want to receive any notification by email? 
        <input type='radio' name='sign_up_notif' value='1' checked>Yes <input type='radio' name='sign_up_notif' value='0'>No
        </div><p><div class="input-group">
        Notification includes: 
        </div><p><div class="input-group">
        You are mentioned by someone
        </div><p><div class="input-group">
        Someone replies your bleats
        </div><p><div class="input-group">
        You gain a new listener
        </div><p><div class="input-group">
        <input type='submit' value='Sign Up' class='btn btn-success'>    
        <input type='hidden' name='goto_signup' value='1'></form> <p>
        <form method='POST' action='bitter.cgi'>
        <input type='submit' value=' Back ' class='btn btn-success'> <p>
        </form>
    </div>
    <div class="col-md-6">
    </div>
    </div>
    </div>       
eof
    if (defined param('sign_up_username') && defined param('sign_up_password1') && defined param('sign_up_password2') && defined param('sign_up_email')) {   
        if (param('sign_up_username') ne '' && param('sign_up_password1') ne '' && param('sign_up_password2') ne '' && param('sign_up_email') ne '') {
            if (param('sign_up_password1') ne param('sign_up_password2')) {
                print "<div class='alert alert-success' role='alert'>Please confirm your password again</div> <p>";
            }
            else {
                my $flag = 0;
                $sign_up_username = param('sign_up_username');
                my $sql = "SELECT * FROM USERS_LARGE WHERE Username = ?";
                my $sth = $dbh->prepare($sql);
                $sth->execute($sign_up_username);
                while (my @row = $sth->fetchrow_array) {
                    $flag = 1;
                    print "<div class='alert alert-success' role='alert'>Sorry, $sign_up_username already exists</div> <p>";
                    last;
                }
                if ($flag == 0) {
                    my $sign_up_username = param('sign_up_username');
                    my $sign_up_email = param('sign_up_email');
                    my $sign_up_password = param('sign_up_password1');
                    my $sign_up_fullname = param('sign_up_fullname');
                    my $sign_up_suburb = param('sign_up_suburb') || '';
                    my $sign_up_latitude = param('sign_up_latitude') || '';
                    my $sign_up_longtitude = param('sign_up_longtitude') || '';
                    my $sign_up_image = param('sign_up_image') || '';
                    my $sign_up_notif = param('sign_up_notif');
                    chomp $sign_up_username;
                    chdir("$users_dir") or die "dead";
                    mkdir("$sign_up_username", 0777) or die "dead2";
                    chdir("$sign_up_username") or die "dead3";
                    open D, ">details.txt" or die "dead4";
                    print D "username: $sign_up_username\npassword: $sign_up_password\nfull_name: $sign_up_fullname\nhome_suburb: $sign_up_suburb\nhome_latitude: $sign_up_latitude\nhome_longtitude: $sign_up_longtitude\nemail: $sign_up_email\n";
                    close D;
                    open NPI, ">profile.jpg" or die "cannot write image";
                    while ($line = <$sign_up_image>) {
                        print NPI $line;
                    }
                    close NPI;
                    my $image = "$users_dir/$sign_up_username/profile.jpg";
                    my $rows = $dbh->do("INSERT INTO USERS_LARGE (Username, Password, Email, Fullname, Suburb, Latitude, Longtitude, ListenTo, Bleats, Image, Notification, Ban) VALUES ('$sign_up_username', '$sign_up_password', '$sign_up_email', '$sign_up_fullname', '$sign_up_suburb', '$sign_up_latitude', '$sign_up_longtitude', '', '', '$image', '$sign_up_notif', '1')");
                    my $subject = "Thank you for join Bitter";
                    my $text = "Hello $sign_up_username, Thank you for join Bitter.\nNow go to this link to confirm your registration:\n$current_url?goto_confirm=1&confirm_username=$sign_up_username&confirm_email=$sign_up_email";
                    send_mail($sign_up_email, $subject, $text, 'z5013846@zmail.unsw.edu.au');
                    print "<div class='alert alert-success' role='alert'>An confirmation email has been sent to $sign_up_email, please check</div> <p>";
                }
            }
        }
    }
}

# if the user receives confirmation email and come to this page
# via url in the email
# check the parameter username and email
# then insert this user to database and set 'Ban' as 0
# means that this account is not suspend currently 
sub print_confirm_page {
    $confirm_username = param('confirm_username');
    $confirm_email = param('confirm_email');
    print "<div class='input-group'>
        Thank you for confirming your Bitter account</div><p><div class='input-group'> 
        Your username is: <strong>$confirm_username</strong></div><p><div class='input-group'>
        Your email is: <strong>$confirm_email</strong></div><p>";
    my $sql = "SELECT * FROM USERS_LARGE WHERE Username = ?";
    my $sth = $dbh->prepare($sql);
    $sth->execute($confirm_username);
    while (my @row = $sth->fetchrow_array) {
        if ($row[2] eq $confirm_email) {
            my $uprows = $dbh->do("UPDATE USERS_LARGE SET Ban = '0' WHERE Username = '$confirm_username'");
        }
    }
    print "<form method='POST' action='bitter.cgi'><input type='submit' value='Log In Now' class='btn btn-success'></form><p>"
}

# if the user forget his password, a reset password email will be sent to his email
sub forget_password {
    print <<eof;
    <form method='POST' action=''>
    <div class="input-group">
        <input type="text" name='reset_username' class="form-control" placeholder="Username (*)" aria-describedby="sizing-addon1"><p>
    </div><p><div class="input-group">    
        <input type='submit' name='goto_reset' value='Reset Password' class='btn btn-success'>
        <input type='hidden' name='Forget Password'>
    </div><p>    
    </form>
    <form method='POST' action='bitter.cgi'>
    <div class="input-group">
        <input type='submit' value='Back' class='btn btn-success'>
    </div><p>
    </form>
eof
    if (defined param('reset_username') && param('reset_username') ne '') {
        my $sql = "SELECT * FROM USERS_LARGE WHERE Username = ?";
        my $sth = $dbh->prepare($sql);
        $sth->execute(param('reset_username'));
        my $flag = 0;
        while (my @row = $sth->fetchrow_array) {
            $flag = 1;
            my $reset_password = $row[1];
            my $reset_email = $row[2];
            my $subject = "Password Recovery Email from Bitter";
            my $text = "This is your current password: $reset_password\n";
            send_mail($reset_email, $subject, $text, 'z5013846@zmail.unsw.edu.au');
            print "<div class='alert alert-success' role='alert'>A Reset Password email has been sent to $reset_email</div><p>";
        }
        if ($flag == 0) {
            my $temp = param('reset_username');
            print "<div class='alert alert-success' role='alert'>Sorry, there is no such user $temp, please try again</div> <p>";
        }
    }
}

# check the username and password that the user entered
# match with users in the database
# only if username and password both matches
# the user will be logging in
sub login_page {
    
    my $flag = 0;

    $login_username = param('login_username') || '';
    $login_password = param('login_password') || '';

    # if the current user has changed his profile details,
    # then update his profile in DB first
    if (defined param('edit_profile')) {
        update_profile();
    }

    # if the current user has deleted his own bleats
    # then delete that bleat in DB first
    if (defined param('delete_my_bleat')) {
        $delete_bleat_id = param('delete_bleat_id');
        delete_bleat($delete_bleat_id);
    }

    # processing the login
    my $sql = "SELECT * FROM USERS_LARGE WHERE Username = ?";
    my $sth = $dbh->prepare($sql);
    $sth->execute($login_username);
    while (my @row = $sth->fetchrow_array) {
        if ($row[1] eq $login_password) {
            $current_username = $login_username;
            $current_password = $login_password;
            param('current_username', $current_username);
            param('current_password', $current_password);
            $profile_password = $row[1];
            $profile_email = $row[2];
            $profile_fullname = $row[3];
            $profile_home_suburb = $row[4];
            $profile_home_latitude = $row[5];
            $profile_home_longtitude = $row[6];
            $profile_listen_to = $row[7];
            $profile_bleats = $row[8];
            $profile_image = $row[9];
            $profile_notification = $row[10];
            $profile_ban = $row[11];
            $flag = 1;
            my_profile_page($current_username);
            print 
            "<form method='POST'>
            <input type='submit' name='Home Page' value='Home Page' class='btn btn-success'>
            <input type='submit' name='Search Page'value='Search Page' class='btn btn-success'>
            <input type='submit' name='Discover Page' value='Discover Page' class='btn btn-success'>
            <input type='hidden' name='login_username' value='$current_username'>
            <input type='hidden' name='login_password' value='$current_password'>
            </form><p>";
            send_new_bleat_page($current_username);
            if (defined param('Search Page') && param('Search Page') eq 'Search Page') {
                ;
            }
            elsif (defined param('Discover Page') && param('Discover Page') eq 'Discover Page') {
                ;
            }
            elsif (defined param('detail_profile_username') && param('detail_profile_username') ne '') {
                ;
            }
            elsif (defined param('result_detail_id') && param('result_detail_id') ne '') {
                ;
            }
            elsif (defined param('result_detail_username') && param('result_detail_username') ne '') {
                ;
            }
            else {
                print "flag";
                recent_bleat_page($current_username);
            }
        }
        else {
            $flag = 1;
            print "<div class='alert alert-success' role='alert'>Incorrect password, please try again </div><p>
            <form method='POST' action='bitter.cgi'><input type='submit' value='Back' class='btn btn-success'></form><p>";
        }
    }
    if ($flag == 0) {
        print "<div class='alert alert-success' role='alert'>Username $login_username does not exists, please try again </div><p>
            <form method='POST' action='bitter.cgi'><input type='submit' value='Back' class='btn btn-success'></form><p>";
    }
}

# if the user delete one of his bleat, then update the bleats database
sub delete_bleat($delete_bleat_id) {
    #print $delete_bleat_id;
    my $row = $dbh->do("DELETE FROM BLEATS_LARGE WHERE ID = '$delete_bleat_id'");
}

# print the send new bleat page
sub send_new_bleat_page($current_username) {
    $new_bleat_replyto = param('new_bleat_replyto') || '';
    $new_bleat_latitude = param('new_bleat_latitude') || '';
    $new_bleat_longtitude = param('new_bleat_longtitude') || '';
    
    my $s = "SELECT MAX(ID) FROM BLEATS_LARGE";
    my $t = $dbh->prepare($s);
    $t->execute();
    while (my @r = $t->fetchrow_array) {
        $new_bleat_filename = $r[0] + 10;
        #print $new_bleat_filename;
    }
    print <<eof;
    <div class="row">
        <div class='container'>
            <legend>Sending New Bleat</legend>
        </div>
    <form method='POST' action='' enctype="multipart/form-data">
        <div class='col-sm-4'>
            <div class="input-group">
                <span class="input-group-addon" id="basic-addon1">Reply to</span>
                <input type="text" name='new_bleat_replyto' class="form-control" placeholder="$new_bleat_replyto" aria-describedby="sizing-addon1"><p>
            </div><p><div class="input-group">
                <span class="input-group-addon" id="basic-addon1">Latitude</span>
                <input type="text" name='new_bleat_latitude' class="form-control" placeholder="$new_bleat_latitude" aria-describedby="sizing-addon1"><p>
            </div><p><div class="input-group">
                <span class="input-group-addon" id="basic-addon1">Longitude</span>
                <input type="text" name='new_bleat_longitude' class="form-control" placeholder="$new_bleat_longtitude" aria-describedby="sizing-addon1"><p>
            </div><p>
                <div class='input-group'>Bleat Attachment: <input type='file' name='new_bleat_image'> </div><p>
        </div>
        <div class='col-sm-8'>
            <div class="form-group">
                <label for="comment">Sending new bleat here(limited to 142 characters)</label>
                <textarea name='new_bleat' class="form-control" rows="5" id="comment"></textarea> 
            </div>
            <input type='submit' value='Send' class='btn btn-success'>
            <input type='hidden' name='login_username' value='$current_username'>
            <input type='hidden' name='login_password' value='$current_password'>
        </div>
    </form>
    </div>
eof
    if (defined param('new_bleat') && param('new_bleat') ne '') {
        $new_bleat = param("new_bleat");
        $new_bleat_time = time();

        open OUT, ">$bleats_dir/$new_bleat_filename" or die "cannot open $new_bleat_filename";
        print OUT "time: $new_bleat_time \nusername: $current_username \nbleat: $new_bleat \n";
        close OUT;
        open O, ">>$users_dir/$current_username/bleats.txt";
        print O "$new_bleat_filename\n";
        close O;

        $new_bleat_attch ='';
        if (defined param('new_bleat_image') && param('new_bleat_image') ne '') {
            $new_bleat_image = param('new_bleat_image');
            open BI, ">$users_dir/$current_username/$new_bleat_time.jpg" or die "cannot write image";
            while ($line = <$new_bleat_image>) {
                print BI $line;
            }
            close BI;
            $new_bleat_attch = "$users_dir/$current_username/$new_bleat_time.jpg";
        }
        my $rows = $dbh->do("INSERT INTO BLEATS_LARGE (ID, Time, Username, Bleat, ReplyTo, Latitude, Longtitude, Attachment, Ban) VALUES ('$new_bleat_filename', '$new_bleat_time', '$current_username', '$new_bleat', '$new_bleat_replyto', '$new_bleat_latitude', '$new_bleat_longitude', '$new_bleat_attch', '0')");
        #print "$new_bleat_time has been inserted into DB <p>";

        # if the new bleat mentions someone, check if he is notificated and send him email
        if ($new_bleat =~ /(\@[a-z][a-z0-9]+) /i) {
            my $name = $1;
            chomp $name;
            $name =~ s/\@//;
            my $sql = "select * from USERS_LARGE where username = '$name'";
            my $sth = $dbh->prepare($sql);
            $sth->execute();
            while (my $ref = $sth->fetchrow_hashref) {
                if ($ref->{'Notification'} eq '1') {
                    my $mail = $ref->{'Email'};
                    my $subject = "New mention on Bitter";
                    my $text = "$current_username has mentioned you on Bitter";
                    send_mail($mail, $subject, $text, 'z5013846@zmail.unsw.edu.au');
                }

            }
        }
    }

    # if replying to someone, than check notification and send him an email
    if (defined param('new_bleat_replyto') && defined param('new_bleat_replyto_username')) {
        if (param('new_bleat_replyto') ne '' && param('new_bleat_replyto_username') ne '') {
            print param('new_bleat_replyto'), param('new_bleat_replyto_username');
            my $reply_to_name = param('new_bleat_replyto_username') || '';
            my $sql = "SELECT * FROM USERS_LARGE WHERE username = '$reply_to_name'";
            my $sth = $dbh->prepare($sql);
            $sth->execute();
            while (my $ref = $sth->fetchrow_hashref()) {
                if ($ref->{'Notification'} eq '1') {
                    my $mail = $ref->{'Email'};
                    my $subject = "You gain a new reply on Bitter";
                    my $text = "$current_username has replied to you on Bitter";
                    send_mail($mail, $subject, $text, 'z5013846@zmail.unsw.edu.au');
                }
            }
        }
    }
}

# if the user update his profile details
sub update_profile {
    $current_username = param('login_username');
    $update_password = param('update_password');
    $update_fullname = param('update_fullname');
    $update_suburb = param('update_suburb');
    $update_latitude = param('update_latitude');
    $update_longtitude = param('update_longtitude');
    $update_notif = param('update_notif');
    $update_susp = param('update_susp'); 
    $update_delete = param('update_delete');
    $update_image = param('update_image');

    if ($update_password ne '') {
        my $rows = $dbh->do("UPDATE USERS_LARGE SET Password = '$update_password' WHERE Username = '$current_username'");
    }
    if ($update_fullname ne '') {
        my $rows = $dbh->do("UPDATE USERS_LARGE SET Fullname = '$update_fullname' WHERE Username = '$current_username'");
    }
    if ($update_suburb ne '') {
        my $rows = $dbh->do("UPDATE USERS_LARGE SET Suburb = '$update_suburb' WHERE Username = '$current_username'");
    }
    if ($update_latitude ne '') {
        my $rows = $dbh->do("UPDATE USERS_LARGE SET Latitude = '$update_latitude' WHERE Username = '$current_username'");
    }
    if ($update_longtitude ne '') {
        my $rows = $dbh->do("UPDATE USERS_LARGE SET Longtitude = '$update_longtitude' WHERE Username = '$current_username'");
    }
    if ($update_notif ne '') {
        my $rows = $dbh->do("UPDATE USERS_LARGE SET Notification = '$update_notif' WHERE Username = '$current_username'");
    }
    if ($update_susp ne '') {
        my $rows = $dbh->do("UPDATE USERS_LARGE SET Suspend = '$update_susp' WHERE Username = '$current_username'");
        my $rows_2 = $dbh->do("UPDATE BLEATS_LARGE SET Ban = '$update_susp' WHERE Username = '$current_username'");
    }
    if ($update_delete eq '1') {
        my $rows = $dbh->do("DELETE FROM USERS_LARGE WHERE Username = '$current_username'");
    }
    if ($update_image ne '') {
        open I, ">$users_dir/$current_username/new_profile.jpg" or die "cannot write image";
        while ($line = <$update_image>) {
            print I $line;
        }
        close I;
        my $new_profile_file = "$users_dir/$current_username/new_profile.jpg";
        my $row = $dbh->do("UPDATE USERS_LARGE SET Image = '$new_profile_file' WHERE Username = '$current_username'");
    }
}

# display all the relevant of one user
# including all the bleats he has sent
# bleats from who he is listening to
# who has replied or @ him
# all together and sorted by reverse-chronological order
sub recent_bleat_page($current_username) {
    print "<legend>Relevant Bleats</legend>";
    my $nb_page = param('nb_page') || 0;
    my $start_index = $nb_page * 10;
    my $sql = "SELECT * FROM BLEATS_LARGE WHERE ((Bleat like '%\@$current_username%') 
    or (Username = '$current_username')
    or (Listener regexp '$current_username')) and Ban = '0' order by ID desc limit $start_index, 10";
    my $sth = $dbh->prepare($sql);
    $sth->execute();
    while (my $ref = $sth->fetchrow_hashref()) { 
        my $q = "select * from USERS_LARGE where Username = ?";
        my $s = $dbh->prepare($q);
        $s->execute($ref->{'Username'});
        my $img = "";
        while (my $r = $s->fetchrow_hashref()) {
            $img = $r->{'Image'};
        }
        my $time = $ref->{'Time'};
        $time = strftime("%m/%d/%Y %H:%M:%S", localtime($time));

        print <<eof;
        <div class='row'>
            <div class='col-sm-6'>
            <img src='$img' class='img-thumbnail'> <p>
            <form method = 'POST'>
                <input type='submit' value='View Profile' class='btn btn-success'> <p>
                <input type='hidden' name='detail_profile_username' value="$ref->{'Username'}">
                <input type='hidden' name='login_username' value='$current_username'>
                <input type='hidden' name='login_password' value='$current_password'>
            </form> <p>
            </div>
            <div class='col-sm-6'>
            <div class='input-group'>ID: $ref->{'ID'} </div><p>
            <div class='input-group'>Time : $time </div><p>
            <div class='input-group'>Username: $ref->{'Username'} </div><p>
            <div class='input-group'>Bleat: $ref->{'Bleat'} </div><p>
eof
        if ($ref->{'ReplyTo'} ne '') {
            print "<div class='input-group'>In reply to: $ref->{'ReplyTo'} </div><p>";
        }
        if ($ref->{'Latitude'} ne '') {
            print "<div class='input-group'>Latitude: $ref->{'Latitude'} </div><p>";
        }
        if ($ref->{'Longtitude'} ne '') {
            print "<div class='input-group'>Longitude: $ref->{'Longtitude'} </div><p>";
        }
        if ($ref->{'Image'} && $ref->{'Image'} ne '') {
            print "<img src=$ref->{'Image'} class='img-thumbnail'> <p>";
        }
print <<eof;
        <form method='POST'>
            <input type='submit' value='View Replies' class='btn btn-success'>
            <input type='hidden' name='result_detail_id' value=$ref->{'ID'}>
            <input type='submit' value='Reply to Bleat' class='btn btn-success'>
            <input type='hidden' name='new_bleat_replyto' value=$ref->{'ID'}>
            <input type='hidden' name='new_bleat_replyto_username' value=$ref->{'Username'}>
eof
        if ($ref->{'Username'} eq $current_username) {
            print "<input type='submit' name='delete_my_bleat' value='Delete Bleat' class='btn btn-success'>
                   <input type='hidden' name='delete_bleat_id' value=$ref->{'ID'}>";
        }
print <<eof
            <input type='hidden' name='login_username' value='$current_username'>
            <input type='hidden' name='login_password' value='$current_password'>
        </form>
            </div> 
        </div>
eof
    }
    my $next_page = $nb_page + 1;
    print 
    "<form method='POST'>
    <input type='submit' value='Next' class='btn btn-success'> <p>
    <input type='hidden' name='nb_page' value='$next_page'>
    <input type='hidden' name='login_username' value='$current_username'>
    <input type='hidden' name='login_password' value='$current_password'>
    </form><p>";
    if ($nb_page != 0) {
        my $prev_page = $nb_page - 1;
        print 
        "<form method='POST'>
        <input type='submit' value='Prev' class='btn btn-success'> <p>
        <input type='hidden' name='nb_page' value='$prev_page'>
        <input type='hidden' name='login_username' value='$current_username'>
        <input type='hidden' name='login_password' value='$current_password'>
        </form><p>";
    }
    if (defined param('detail_profile_username')) {
        username_detail();
    }
    if (defined param('result_detail_id')) {
        bleat_replies();
    }
}

# display current user details and can be edit at the same time
sub my_profile_page($current_username) {
    if (defined param('add to') && param('add to') eq 'Listen') {
        $result_detail_username = param('detail_profile_username');
        if ($profile_listen_to !~ /$result_detail_username/) {
            $profile_listen_to .= " ".$result_detail_username;
            my $rows = $dbh->do("UPDATE USERS_LARGE SET ListenTo = '$profile_listen_to' WHERE Username = '$current_username'");
        }

        # update the bleats table with listener
        my $s_q_l = "select * from BLEATS_LARGE where Username = '$result_detail_username'";
        my $s_t_h = $dbh->prepare($s_q_l);
        $s_t_h->execute();
        while (my $r_e_f = $s_t_h->fetchrow_hashref()) {
            my $listener = $r_e_f->{'Listener'};
            $listener = $listener." ".$current_username;
            my $r_o_w = $dbh->do("update BLEATS_LARGE set Listener = '$listener' where Username= '$result_detail_username'");
        }

        my $sql = "SELECT * FROM USERS_LARGE WHERE username = '$result_detail_username'";
        my $sth = $dbh->prepare($sql);
        $sth->execute();
        while (my $ref = $sth->fetchrow_hashref()) {
            if ($ref->{'Notification'} eq '1') {
                my $mail = $ref->{'Email'};
                my $subject = "You gain a new listener on Bitter";
                my $text = "$current_username has listened to you on Bitter";
                send_mail($mail, $subject, $text, 'z5013846@zmail.unsw.edu.au');
            }
        }
    }
    if (defined param('add to') && param('add to') eq 'Unlisten') {
        $result_detail_username = param('detail_profile_username');
        $profile_listen_to =~ s/ $result_detail_username//;
        my $rows = $dbh->do("UPDATE USERS_LARGE SET ListenTo = '$profile_listen_to' WHERE Username = '$current_username'");
    }

    print <<eof;
    <legend>My Profile</legend>
    <div class="row">
        <div class="col-sm-4">
            <div class='input-group'>
                <form method='POST' action='bitter.cgi' >
                <img src='$profile_image' class="img-thumbnail"> <p>
                <ul class="list-group">
                    <li class="list-group-item"><strong>Log In as: $current_username</strong></li>
                    <li class="list-group-item"><strong>Email: $profile_email</strong></li>
                </ul> 
                <input type='submit' value='Log Out' class='btn btn-success'>
                </form><p>
            </div>
        </div>
        <div class="col-sm-8">
                <form method='POST' action='' enctype="multipart/form-data">
                <div class="input-group">
                    <span class="input-group-addon" id="basic-addon1">Password</span>
                    <input type="password" name='update_password' class="form-control" placeholder="" aria-describedby="sizing-addon1"><p>
                </div><p><div class="input-group">
                    <span class="input-group-addon" id="basic-addon1">Fullname</span>
                    <input type="text" name='update_fullname' class="form-control" placeholder="$profile_fullname" aria-describedby="sizing-addon1"><p>
                </div><p><div class="input-group">
                    <span class="input-group-addon" id="basic-addon1">Home Suburb</span>
                    <input type="text" name='update_suburb' class="form-control" placeholder="$profile_home_suburb" aria-describedby="sizing-addon1"><p>
                </div><p><div class="input-group">
                    <span class="input-group-addon" id="basic-addon1">Home Latitude</span>
                    <input type="text" name='update_latitude' class="form-control" placeholder="$profile_home_latitude" aria-describedby="sizing-addon1"><p>
                </div><p><div class="input-group">
                    <span class="input-group-addon" id="basic-addon1">Home Longitude</span>
                    <input type="text" name='update_longtitude' class="form-control" placeholder="$profile_home_longtitude" aria-describedby="sizing-addon1"><p>
                </div><p><div class="input-group">
                    Update my profile image: <input type='file' name='update_image'>
                </div><p><div class="input-group">
                    Notification: <input type='radio' name='update_notif' value='1' checked>Yes <input type='radio' name='update_notif' value='0'>No
                </div><p><div class="input-group">            
                    Suspend My Account: <input type='radio' name='update_susp' value='1'>Yes <input type='radio' name='update_susp' value='0'>No
                </div><p><div class="input-group">
                    Delete My Account:
                    (*Cannot be recovered! Are you sure to delete your account?)
                    <input type='radio' name='update_delete' value='1'>Yes <p>
                </div><p>
eof
    if (defined param('update_image') && param(update_image) ne '') {
        my $new_profile_img = param('update_image');
        open THIS, ">new_profile_image.jpg" or die "cannot write new image";
        while ($line = <$new_profile_img>) {
            print THIS $line;
        }
        close THIS;
    }
print <<eof
                    <input type='submit' name='edit_profile' value='Edit My Profile' class='btn btn-success'> <p>
                    <input type='hidden' name='login_username' value='$current_username'>
                    <input type='hidden' name='login_password' value='$current_password'> 
                    <div class='input-group'>Listen To: $profile_listen_to </div><p>    
        </div>
    </div>
eof
}

# show search results
sub search_result() {
    param('Search Page', 'Search Page');
    my $flag = 0;
    $search_by = param('search_by') || '';
    $page = param('page') || 0;
    $go_to_page = param('go_to_page') || '';
    my $count = 0;
    print "<legend>Search Result</legend>";
    if ($search_by eq 'search_username') {
        $search_username = param('search_content');
        print "<strong>You searched for Username: ", $search_username, "</strong><p>";
        
        my $sql = "SELECT * FROM USERS_LARGE WHERE username like '%$search_username%' limit $page, 10";
        my $sth = $dbh->prepare($sql);
        $sth->execute();
        while (my $ref = $sth->fetchrow_hashref()) {
            $flag = 1;
            my $temp = $ref->{'Username'};
            print 
            "<div class='input-group'>Username: $ref->{'Username'} </div><p>
            <div class='input-group'>Fullname: $ref->{'Fullname'} </div><p>
            <form method='POST'>
                <input type='submit' value='View Profile' class='btn btn-success'>
                <input type='hidden' name='result_detail_username' value='$temp'>
                <input type='hidden' name='login_username' value='$current_username'>
                <input type='hidden' name='login_password' value='$current_password'>
                <input type='hidden' name='search_by' value='$search_by'>
                <input type='hidden' name='search_content' value='$search_username'>
            </form><p>";
            $count++;
        }
        if ($page == 0) {
            $page = 10;
            print 
            "<form method='POST'>
            <input type='submit' name='go_to_page' value='Next' class='btn btn-success'><p>
            <input type='hidden' name='page' value=$page>
            <input type='hidden' name='login_username' value='$current_username'>
            <input type='hidden' name='login_password' value='$current_password'>
            <input type='hidden' name='search_by' value='$search_by'>
            <input type='hidden' name='search_content' value='$search_username'>
            </form><p>";
        }
        else {
            if ($count == 10) {
                if ($go_to_page eq 'Next') {
                    $page += 10;
                }
                if ($go_to_page eq 'Prev') {
                    $page -= 10;
                }
                print 
                    "<form method='POST'>
                    <input type='submit' name='go_to_page' value='Prev' class='btn btn-success'>
                    <input type='submit' name='go_to_page' value='Next' class='btn btn-success'>
                    <input type='hidden' name='Page' value=$page>
                    <input type='hidden' name='login_username' value='$current_username'>
                    <input type='hidden' name='login_password' value='$current_password'>
                    <input type='hidden' name='search_by' value='$search_by'>
                    <input type='hidden' name='search_content' value='$search_username'>
                    </form><p>";
            }
            if ($count < 10) {
                    $page -= 10;
                print 
                    "<form method='POST'>
                    <input type='submit' name='go_to_page' value='Prev' class='btn btn-success'>
                    <input type='hidden' name='Page' value=$page>
                    <input type='hidden' name='login_username' value='$current_username'>
                    <input type='hidden' name='login_password' value='$current_password'>
                    <input type='hidden' name='search_by' value='$search_by'>
                    <input type='hidden' name='search_content' value='$search_username'>
                    </form><p>";
            }
        }
    }
    if ($search_by eq 'search_fullname') {
        $search_fullname = param('search_content');
        print  "<strong>You searched for Fullname: ", $search_fullname, "</strong><p>";
        my $sql = "SELECT * FROM USERS_LARGE WHERE Fullname LIKE '%$search_fullname%' limit $page, 10";
        my $sth = $dbh->prepare($sql);
        $sth->execute();
        while (my $ref = $sth->fetchrow_hashref()) {
            $flag = 1;
            print "<div class='input-group'>Username: $ref->{'Username'}", "</div><p>",
            "<div class='input-group'>Fullname: $ref->{'Fullname'} </div><p>",
            "<form method='POST'>
            <input type='submit' value='View Profile' class='btn btn-success'>
            <input type='hidden' name='result_detail_username' value=$ref->{'Username'}>
            <input type='hidden' name='login_username' value='$current_username'>
            <input type='hidden' name='login_password' value='$current_password'>
            <input type='hidden' name='search_by' value='$search_by'>
            <input type='hidden' name='search_content' value='$search_fullname'>
            </form><p>";
            $count++;
        }
        if ($page == 0) {
            $page = 10;
            print 
            "<form method='POST'>
            <input type='submit' name='go_to_page' value='Next' class='btn btn-success'><p>
            <input type='hidden' name='page' value=$page>
            <input type='hidden' name='login_username' value='$current_username'>
            <input type='hidden' name='login_password' value='$current_password'>
            <input type='hidden' name='search_by' value='$search_by'>
            <input type='hidden' name='search_content' value='$search_fullname'>
            </form><p>";
        }
        else {
            if ($count == 10) {
                if ($go_to_page eq 'Next') {
                    $page += 10;
                }
                if ($go_to_page eq 'Prev') {
                    $page -= 10;
                }
                print 
                    "<form method='POST'>
                    <input type='submit' name='go_to_page' value='Prev' class='btn btn-success'>
                    <input type='submit' name='go_to_page' value='Next' class='btn btn-success'
                    <input type='hidden' name='Page' value=$page>
                    <input type='hidden' name='login_username' value='$current_username'>
                    <input type='hidden' name='login_password' value='$current_password'>
                    <input type='hidden' name='search_by' value='$search_by'>
                    <input type='hidden' name='search_content' value='$search_fullname'>
                    </form><p>";
            }
            if ($count < 10) {
                    $page -= 10;
                print 
                    "<form method='POST'>
                    <input type='submit' name='go_to_page' value='Prev' class='btn btn-success'>
                    <input type='hidden' name='Page' value=$page>
                    <input type='hidden' name='login_username' value='$current_username'>
                    <input type='hidden' name='login_password' value='$current_password'>
                    <input type='hidden' name='search_by' value='$search_by'>
                    <input type='hidden' name='search_content' value='$search_fullname'>
                    </form><p>";
            }
        }
    }
    if ($search_by eq 'search_bleat') {
        $search_bleat = param('search_content');
        print  "<strong>You searched for Bleat: ", $search_bleat, "</strong><p>";
        my $sql = "SELECT * FROM BLEATS_LARGE WHERE Bleat like '%$search_bleat%' limit $page, 10";
        my $sth = $dbh->prepare($sql);
        $sth->execute();
        while (my $ref = $sth->fetchrow_hashref()) {
            $flag = 1;
            my $s = "SELECT Image FROM USERS_LARGE WHERE Username = ?";
            my $t = $dbh->prepare($s);
            $t->execute($ref->{'Username'});
            while (my $r = $t->fetchrow_hashref()) {
                $im = $r->{'Image'};
            }
            print 
            "<p><p><img src='$im' class='img-thumbnail'> <p>
            <div class='input-group'>ID: $ref->{'ID'} </div><p>";
            my $time = strftime("%m/%d/%Y %H:%M:%S", localtime($ref->{'Time'}));
            print 
            "<div class='input-group'>Time: $time </div><p>
            <div class='input-group'>Username: $ref->{'Username'} </div><p>";
            if ($ref->{'ReplyTo'} ne '') {
                print "<div class='input-group'>In Reply To: $ref->{'ReplyTo'} <div><p>";
            }
            if ($ref->{'Latitude'} ne '') {
                print "<div class='input-group'>Latitude: $ref->{'Latitude'} </div><p>";
            }
            if ($ref->{'Longtitude'} ne '') {
                print "<div class='input-group'>Longitude: $ref->{'Longtitude'} </div><p>";
            }
            print 
            "<div class='input-group'>Bleat: $ref->{'Bleat'} </div><p>
            <form method='POST'>
                <input type='submit' value='View Replies' class='btn btn-success'>
                <input type='hidden' name='result_detail_id' value=$ref->{'ID'}>
                <input type='submit' value='Reply to Bleat' class='btn btn-success'>
                <input type='hidden' name='new_bleat_replyto' value=$ref->{'ID'}>
                <input type='hidden' name='new_bleat_replyto_username' value=$ref->{'Username'}>
                <input type='hidden' name='login_username' value='$current_username'>
                <input type='hidden' name='login_password' value='$current_password'>
                <input type='hidden' name='search_by' value='$search_by'>
                <input type='hidden' name='search_content' value='$search_bleat'>
            </form><p><p>";
            $count++;
        }
        if ($page == 0) {
            $page = 10;
            print 
            "<form method='POST'>
            <input type='submit' name='go_to_page' value='Next' class='btn btn-success'><p>
            <input type='hidden' name='page' value=$page>
            <input type='hidden' name='login_username' value='$current_username'>
            <input type='hidden' name='login_password' value='$current_password'>
            <input type='hidden' name='search_by' value='$search_by'>
            <input type='hidden' name='search_content' value='$search_bleat'>
            </form><p>";
        }
        else {
            if ($count == 10) {
                if ($go_to_page eq 'Next') {
                    $page += 10;
                }
                if ($go_to_page eq 'Prev') {
                    $page -= 10;
                }
                print 
                    "<form method='POST'>
                    <input type='submit' name='go_to_page' value='Prev' class='btn btn-success'>
                    <input type='submit' name='go_to_page' value='Next' class='btn btn-success'>
                    <input type='hidden' name='Page' value=$page>
                    <input type='hidden' name='login_username' value='$current_username'>
                    <input type='hidden' name='login_password' value='$current_password'>
                    <input type='hidden' name='search_by' value='$search_by'>
                    <input type='hidden' name='search_content' value='$search_bleat'>
                    </form><p>";
            }
            if ($count < 10) {
                    $page -= 10;
                print 
                    "<form method='POST'>
                    <input type='submit' name='go_to_page' value='Prev' class='btn btn-success'>
                    <input type='hidden' name='Page' value=$page>
                    <input type='hidden' name='login_username' value='$current_username'>
                    <input type='hidden' name='login_password' value='$current_password'>
                    <input type='hidden' name='search_by' value='$search_by'>
                    <input type='hidden' name='search_content' value='$search_bleat'>
                    </form><p>";
            }
        }
    }
    if ($flag == 0) {
        print "<div class='input-group'>Sorry, No results </div><p>";    
    }
    if ($flag == 1) {
        if (defined param('result_detail_username')) {
            username_detail();
        }
        if (defined param('result_detail_id')) {
            bleat_replies();
        }
    }
}

# detail information of the user that is being searched
sub username_detail() {
    $search_by = param('$search_by') || '';
    $search_username = param('$search_content') || '';
    if (defined param('detail_profile_username') && param('detail_profile_username') ne '') {
        $detail_profile_username = param('detail_profile_username');
    }
    if (defined param('result_detail_username') && param('result_detail_username') ne '') {
        $detail_profile_username = param('result_detail_username');
        print $detail_profile_username;
    }
    print "<legend>$detail_profile_username\'s detailed profile:</legend>";
    my $sql = "SELECT * FROM USERS_LARGE WHERE username = ?";
    my $sth = $dbh->prepare($sql);
    $sth->execute($detail_profile_username);
    while (my @row = $sth->fetchrow_array) {
        print 
        "<div class='row'>
        <div class='col-sm-8'>
        <div class='col-sm-6'>
        <img src='$row[9]' class='img-thumbnail'> <p>
            <form method='POST'>
                <input type='submit' name='add to' value='Listen' class='btn btn-success'>
                <input type='submit' name='add to' value='Unlisten' class='btn btn-success'>
                <input type='hidden' name='detail_profile_username' value='$detail_profile_username'>
                <input type='hidden' name='login_username' value='$current_username'>
                <input type='hidden' name='login_password' value='$current_password'>
                <input type='hidden' name='search_by' value='$search_by'>
                <input type='hidden' name='search_content' value='$search_username'>
            </form><p>
        </div>
        <div class='col-sm-6'>
            <div class='input-group'>Username: $row[0] </div><p>
            <div class='input-group'>Fullname: $row[3] </div><p>
            <div class='input-group'>Home Suburb: $row[4] </div><p>
            <div class='input-group'>Home Latitude: $row[5] </div><p>
            <div class='input-group'>Home Longitude: $row[6] </div><p>
            <div class='input-group'>Listen To: $row[7] </div><p>
        </div>
        </div>
        </div><p>";
    }
}

# show replies of one bleat
sub bleat_replies() {
    my $flag = 0;
    $result_detail_id = param('result_detail_id');
    $search_by = param('search_by') || '';
    $search_bleat = param('search_content') || '';
    print "<legend>Relying bleats of ID $result_detail_id</legend>";
    my $sql = "SELECT * FROM BLEATS_LARGE WHERE ReplyTo = ?";
    my $sth = $dbh->prepare($sql);
    $sth->execute($result_detail_id);
    while (my @row = $sth->fetchrow_array) {
        $flag = 1;
        print 
        "<div class='input-group'>Time: $row[1] </div><p>
        <div class='input-group'>Username: $row[2] </div><p>
        <div class='input-group'>Bleat: $row[3] </div><p>
        <div class='input-group'>In Reply To: $row[4] </div><p>
        <form>
            <input type='submit' value='View Replies' class='btn btn-success'>
            <input type='hidden' name='result_detail_id' value=$row[0]>
            <input type='hidden' name='login_username' value='$current_username'>
            <input type='hidden' name='login_password' value='$current_password'>
            <input type='hidden' name='search_by' value='$search_by'>
            <input type='hidden' name='search_content' value='$search_bleat'>
        </form><p>";
    }
    if ($flag == 0) {
        print "Sorry, No Replies to this Bleat <p>";
    }
    #if ($flag == 1) {
     #   if (defined param('result_detail_id')) {
      #      bleat_replies();
       #     #$result_detail_time = param('result_detail_time');
        #}
    #}
}

# display all users
sub user_page {
    my $m = param('next_user_m') || 0;
    my $nb = param('next_bleat_nb') || 0;
    my $sql = "select * from USERS_LARGE limit $m, 1";
    my $sth = $dbh->prepare($sql);
    $sth->execute();
    while (my $ref = $sth->fetchrow_hashref()) {
        print 
        "<legend>Current Users</legend>
        <div class='row'>
        <div class='col-sm-6'>";
        print "<img src=$ref->{'Image'} class='img-thumbnail'>";
        print "</div>
        <div class='col-sm-6'>
        <div class='input-group'>Username: $ref->{'Username'} </div><p>
        <div class='input-group'>Fullname: $ref->{'Fullname'} </div><p>
        <div class='input-group'>Suburb: $ref->{'Suburb'} </div><p>";
        if ($ref->{'Latitude'} ne '') {
            print "<div class='input-group'>Latitude: $ref->{'Latitude'} </div><p>";
        }
        if ($ref->{'Longtitude'} ne '') {
            print "<div class='input-group'>Longitude: $ref->{'Longtitude'} </div><p>";
        }
        $m++;
        print
        "<div class='input-group'>Listen To: $ref->{'ListenTo'} </div><p>
        <form method='POST'>
        <input type='submit' value='Next User' class='btn btn-success'>
        <input type='hidden' name='next_user_m' value='$m'>
        <input type='hidden' name='next_bleat_nb' value='$nb'>
        <input type='hidden' name='login_username' value='$current_username'>
        <input type='hidden' name='login_password' value='$current_password'>
        <input type='hidden' name='Discover Page' value='Discover Page'>
        </form>
        </div></div><p><p>";
    }
}

# display all bleats
sub bleat_page {
    my $nb = param('next_bleat_nb') || 0;
    my $m = param('next_user_m') || 0;
    my $sql = "select * from BLEATS_LARGE limit $nb, 1";
    my $sth = $dbh->prepare($sql);
    $sth->execute();
    while (my $ref = $sth->fetchrow_hashref()) {
        print 
        "<legend>Current Bleats</legend>
        <div class='input-group'>ID: $ref->{'ID'} </div><p>";
        my $time = strftime("%m/%d/%Y %H:%M:%S", localtime($ref->{'Time'}));
        print
        "<div class='input-group'>Time: $time </div><p>
        <div class='input-group'>Username: $ref->{'Username'} </div><p>";
        if ($ref->{'Latitude'} ne '') {
            print "<div class='input-group'>Latitude: $ref->{'Latitude'} </div><p>";
        }
        if ($ref->{'Longtitude'} ne '') {
            print "<div class='input-group'>Longitude: $ref->{'Longtitude'} </div><p>";
        }
        if ($ref->{'ReplyTo'} ne '') {
            print "<div class='input-group'>Reply To: $ref->{'ReplyTo'} </div><p>";
        }
        $nb++;
        print
        "<div class='input-group'>Bleat: $ref->{'Bleat'} </div><p>
        <form method='POST'>
        <input type='submit' value='Next Bleat' class='btn btn-success'>
        <input type='hidden' name='next_user_m' value='$m'>
        <input type='hidden' name='next_bleat_nb' value='$nb'>
        <input type='hidden' name='login_username' value='$current_username'>
        <input type='hidden' name='login_password' value='$current_password'>
        <input type='hidden' name='Discover Page' value='Discover Page'>
        </form><p>";
    }
}


sub page_header {
    return <<eof
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>

<title>Bitter</title>
<link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="/scripts/jquery.min.js"></script>
<script src="/bootstrap/js/bootstrap.min.js"></script>
</head>
<body>
<div class="jumbotron">
    <div class="container">
        <h1>Bitter</h1>
eof
}


sub page_trailer {
    print "</div></div>";
    my $html = "";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}

main();