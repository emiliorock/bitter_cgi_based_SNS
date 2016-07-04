#!/usr/bin/perl -w

use CGI;
use DBI;

$host = 'z5013846.srvr';
$database = 'bitter';
$dataset_size = "large"; 
$users_dir = "dataset-$dataset_size/users";
$bleats_dir = "dataset-$dataset_size/bleats";

my $dbh = DBI->connect("DBI:mysql:database=$database;host=$host;port=3306", "z5013846", "z5013846");

# insert user information into USERS table
$i = 0;
my @users = sort(glob("$users_dir/*"));
foreach $user (@users) {
	my $username = ""; 
	my $password = "";
	my $fullname = "";
	my $email = "";
	my $home_suburb = "";
	my $home_latitude = "";
	my $home_longtitude = "";
	my $listen = "";
	my $profile_image_file = "";
	my $temp = $user;
	$details_file = "$user/details.txt";
	open DETAILS, "<$details_file" or die "cannot open $details_file";
	while ($line = <DETAILS>) {
		chomp $line;
		$temp =~ s/dataset\-large\/users\///;
		if ($line =~ /username: /) {
			$username = $line;
			$username =~ s/username: //;
		}
		if ($line =~ /password: /) {
			$password = $line;
			$password =~ s/password: //;
		}
		if ($line =~ /full_name: /) {
			$fullname = $line;
			$fullname =~ s/full_name: //;
		}
		if ($line =~ /email: /) {
			$email = $line;
			$email =~ s/email: //;
		}
		if ($line =~ /home_suburb: /) {
			$home_suburb = $line;
			$home_suburb =~ s/home_suburb: //;
		}
		if ($line =~ /home_latitude: /) {
			$home_latitude = $line;
			$home_latitude =~ s/home_latitude: //;
		}
		if ($line =~ /home_longtitude: /) {
			$home_longtitude = $line;
			$home_longtitude =~ s/home_longtitude: //;
		}
		if ($line =~ /listens: /) {
			$listen = $line;
			$listen =~ s/listens: //;
			print $temp ,"\n";
			@ones = split(/ /, $listen);
			foreach $one (@ones) {
				#my $r = $dbh->do("INSERT INTO LISTEN_LARGE (ID, Speaker, Listener) VALUES ('$i', '$one', '$temp')");
				#print "$one, $temp is a pair\n";
				#$i++;
			}
		}
	}
	close DETAILS;

	$profile_image_file = "$user/profile.jpg";
	if (open P, "<$profile_image_file") {
		close P;
	}
	else {
		$profile_image_file = "default.png";	
	}
	
	my $bleats_file = "$user/bleats.txt";
	open BLEATS, "<$bleats_file" or die "cannot open $bleats_file";
	$bleats = "";
	while ($line = <BLEATS>) {
		chomp $line;
		$bleats .= $line." ";
	}
	close BLEATS;
	#my $rows = $dbh->do("INSERT INTO USERS_LARGE (Username, Password, Email, Fullname, Suburb, Latitude, Longtitude, ListenTo, Bleats, Image, Notification, Ban) VALUES ('$temp', '$password', '$email', '$fullname', '$home_suburb', '$home_latitude', '$home_longtitude', '$listen', '$bleats', '$profile_image_file', '1', '0')");
	#print "$username has been inserted\n";
}


# insert information into BLEATS table
my @bleats = sort(glob("$bleats_dir/*"));
foreach $bleat_file (@bleats) {
	my $id = $bleat_file;
	$id =~ s/$bleats_dir\///;
	my $username = "";
	my $time = "";
	my $mention = "";
	my $keyword = "";
	my $reply_to = "";
	my $latitude = "";
	my $longtitude = "";
	my $attchment = "";
	open B, "<$bleat_file" or die "cannot open $bleat_file";
	while ($line = <B>) {
		chomp $line;
		if ($line =~ /username: /) {
			$username = $line;
			$username =~ s/username: //;
		}
		if ($line =~ /time: /) {
			$time = $line;
			$time =~ s/time: //;
		}
		if ($line =~ /bleat: /) {
			$bleat = $line;
			$bleat =~ s/bleat: //;
			if ($bleat =~ /\'/) {
				$bleat =~ s/\'/\\\'/g;
			}
			if ($bleat =~ /\"/) {
				$bleat =~ s/\"/\\\"/g;
			}
			if ($bleat =~ /\)/) {
				$bleat =~ s/\)/\\\)/g;
			}
		}
		if ($line =~ /latitude: /) {
			$latitude = $line;
			$latitude =~ s/latitude: //;
		}
		if ($line =~ /longtitude: /) {
			$longtitude = $line;
			$longtitude =~ s/longtitude: //;
		}
		if ($line =~ /in_reply_to: /) {
			$reply_to = $line;
			$reply_to =~ s/in_reply_to: //;
		}
	}
	close B;
	my $rows = $dbh->do("INSERT INTO BLEATS_LARGE (ID, Time, Username, Bleat, ReplyTo, Latitude, Longtitude, Attachment, Ban) VALUES ('$id', '$time', '$username', '$bleat', '$reply_to', '$latitude', '$longtitude', null, '0')");
	print "$id has been inserted\n";
}

#my $res = $dbh->selectall_arrayref('select * from user');

#foreach my $row (@$res) {
#	print join(',', @$row), "\n";
#}

$dbh->disconnect();

#this is for mysql database
#create table USERS_LARGE (Username varchar(50) primary key, Password varchar(50), Email varchar(100), Fullname varchar(50), Suburb varchar(100), Latitude varchar(100), Longtitude varchar(100), ListenTo varchar(500), Bleats varchar(500), Image varchar(200), Notification varchar(50), Ban varchar(50));
#create table BLEATS_LARGE (ID varchar(50) Primary Key, Time varchar(50), Username varchar(50), Bleat varchar(200), ReplyTo varchar(50), Latitude varchar(50), Longtitude varchar(50), Attachment varchar(200), Ban varchar(50));
#create table LISTEN_LARGE (ID varchar(50) primary key, Speaker varchar(50), Listener varchar(50));