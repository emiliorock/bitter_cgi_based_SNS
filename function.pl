sub recent_bleat_page($current_username) {
    my $key_time = param('key_time') || '';

    %recent_bleats_bleat = ();
    %recent_bleats_username= ();
    %recent_bleats_reply = ();
    %recent_bleats_latitude = ();
    %recent_bleats_longtitude = ();
    %recent_bleats_id = ();
    %recent_bleats_image = ();
    %recent_bleats_user_image = ();

    # show recent bleats by the current user
    my $sql = "SELECT * FROM BLEATS_LARGE WHERE username = ?";
    my $sth = $dbh->prepare($sql);
    $sth->execute($current_username);
    while (my @row = $sth->fetchrow_array) {
        $time = $row[1];
        $recent_bleats_id{$time} = $row[0];
        $recent_bleats_username{$time} = $row[2];
        $recent_bleats_bleat{$time} = $row[3];
        $recent_bleats_reply{$time} = $row[4];
        $recent_bleats_latitude{$time} = $row[5];
        $recent_bleats_longtitude{$time} = $row[6];
        $recent_bleats_image{$time} = $row[7];
        $count++;
    }

    # show bleats that mention the current user
    my $sql_2 = "SELECT * FROM BLEATS_LARGE WHERE Bleat like '%\@$current_username%' and Ban = '0'";
    my $sth_2 = $dbh->prepare($sql_2);
    $sth_2->execute();
    while (my @row_2 = $sth_2->fetchrow_array) {
        $time = $row_2[1];
        $recent_bleats_id{$time} = $row_2[0];
        $recent_bleats_username{$time} = $row_2[2];
        $recent_bleats_bleat{$time} = $row_2[3];
        $recent_bleats_reply{$time} = $row_2[4];
        $recent_bleats_latitude{$time} = $row_2[5];
        $recent_bleats_longtitude{$time} = $row_2[6];
        $recent_bleats_image{$time} = $row_2[7];
        $count++;
    }

    # show bleats from the users who the current user is listening to
    @users_listen_to = split(/ /, $profile_listen_to);
    foreach $user_listen_to (@users_listen_to) {
        my $sql_3 = "SELECT * FROM BLEATS_LARGE WHERE Username = ? and Ban = '0'";
        my $sth_3 = $dbh->prepare($sql_3);
        $sth_3->execute($user_listen_to);
        while (my @row_3 = $sth_3->fetchrow_array) {
            $time = $row_3[1];
            $recent_bleats_id{$time} = $row_3[0];
            $recent_bleats_username{$time} = $row_3[2];
            $recent_bleats_bleat{$time} = $row_3[3];
            $recent_bleats_reply{$time} = $row_3[4];
            $recent_bleats_latitude{$time} = $row_3[5];
            $recent_bleats_longtitude{$time} = $row_3[6];
            $recent_bleats_image{$time} = $row_3[7];
            $count++;
        }
    }

    foreach $time (keys %recent_bleats_username) {
         my $sql_4 = "SELECT * FROM USERS_LARGE WHERE Username = ? and Ban = '0'";
         my $sth_4 = $dbh->prepare($sql_4);
         $sth_4->execute($recent_bleats_username{$time});
         while (my @row_4 = $sth_4->fetchrow_array) {
            $recent_bleats_user_image{$time} = $row_4[9];
         }
    }

    my $count = 0;
    my $flag = 0;
    my $flag_2 = 0;
    my $flag_3 = 0;

    print "<legend>Relevant Bleats</legend>";

    foreach $time (sort {$b<=>$a} keys %recent_bleats_bleat) {
        if ($key_time eq '') {
            if ($count == 0) {
                $start[$k] = $time;
                $k++;
            }
            if ($count < 10) {
                print 
                    "<div class='row'>
                    <div class='col-sm-4'>
                    <img src='$recent_bleats_user_image{$time}' class='img-thumbnail'> <p>
                    <form>
                        <input type='submit' value='View Profile' class='btn btn-success'>
                        <input type='hidden' name='result_detail_username' value='$recent_bleats_username{$time}'>
                        <input type='hidden' name='login_username' value='$current_username'>
                        <input type='hidden' name='login_password' value='$current_password'>
                    </form> <p>
                    </div>
                    <div class='col-sm-8'>
                    <div class='input-group'>ID: $recent_bleats_id{$time}</div><p>";
                    $temp = strftime('%m/%d/%Y %H:%M:%S', localtime($time));
                    print "<div class='input-group'>Time: $temp</div><p>";
                    print
                    "<div class='input-group'>Username: $recent_bleats_username{$time} 
                    </div><p>
                    <div class='input-group'>Bleat: $recent_bleats_bleat{$time} </div><p>";
                if ($recent_bleats_reply{$time} ne '') {
                    print "<div class='input-group'>In reply to: $recent_bleats_reply{$time} </div><p>";
                }
                if ($recent_bleats_latitude{$time} ne '') {
                    print "<div class='input-group'>Latitude: $recent_bleats_latitude{$time} </div><p>";
                }
                if ($recent_bleats_longtitude{$time} ne '') {
                    print "<div class='input-group'>Longtitude: $recent_bleats_longtitude{$time} </div><p>";
                }
                if ($recent_bleats_image{$time} && $recent_bleats_image{$time} ne '') {
                    print "<img src='$recent_bleats_image{$time}' class='img-thumbnail'> <p>";
                }
                print
                "<form method='POST' action=''>
                <input type='submit' value='View Replies' class='btn btn-success'>
                <input type='hidden' name='result_detail_id' value='$recent_bleats_id{$time}'>
                <input type='submit' value='Reply to Bleat' class='btn btn-success'>
                <input type='hidden' name='new_bleat_replyto' value='$recent_bleats_id{$time}'>
                <input type='hidden' name='new_bleat_replyto_username' value='$recent_bleats_username{$time}'>";
                if ($recent_bleats_username{$time} eq $current_username) {
                    print "<input type='submit' name='delete_my_bleat' value='Delete Bleat' class='btn btn-success'>
                    <input type='hidden' name='delete_bleat_id' value='$recent_bleats_id{$time}'>";
                }
                print "<input type='hidden' name='login_username' value='$current_username'>
                <input type='hidden' name='login_password' value='$current_password'>
                </form></div></div><p>";
                $count++;
            }
            if ($count == 10) {
                $start[$k] = $time;
                print 
                "<form method='POST'>
                <input type='submit' name='go_to_bleat_page' value='Next' class='btn btn-success'>
                <input type='hidden' name='key_time' value=$start[$k]>
                <input type='hidden' name='login_username' value='$current_username'>
                <input type='hidden' name='login_password' value='$current_password'>
                </form>
                </div><p>";
                $k++;
                last;
            }
        }
        if ($key_time ne '') {
            if (param('go_to_bleat_page') eq 'Next') {
                if ($time eq $key_time) {
                    $flag = 1;
                    next;
                }
                if ($flag == 1 && $count < 10) {
                    print 
                    "<div class='row'>
                    <div class='col-sm-4'>
                    <img src='$recent_bleats_user_image{$time}' class='img-thumbnail'> <p>
                    <form>
                        <input type='submit' value='View Profile' class='btn btn-success'>
                        <input type='hidden' name='result_detail_username' value='$recent_bleats_username{$time}'>
                        <input type='hidden' name='login_username' value='$current_username'>
                        <input type='hidden' name='login_password' value='$current_password'>
                    </form> <p>
                    </div>
                    <div class='col-sm-8'>
                    <div class='input-group'>ID: $recent_bleats_id{$time}</div><p>";
                    $temp = strftime('%m/%d/%Y %H:%M:%S', localtime($time));
                    print "<div class='input-group'>Time: $temp</div><p>";
                    print 
                    "<div class='input-group'>Username: $recent_bleats_username{$time} 
                    </div><p>
                    <div class='input-group'>Bleat: $recent_bleats_bleat{$time} </div><p>";
                        if ($recent_bleats_reply{$time} ne '') {
                            print "<div class='input-group'>In reply to: $recent_bleats_reply{$time} </div><p>";
                        }
                        if ($recent_bleats_latitude{$time} ne '') {
                            print "<div class='input-group'>Latitude: $recent_bleats_latitude{$time} </div><p>";
                        }
                        if ($recent_bleats_longtitude{$time} ne '') {
                            print "<div class='input-group'>Longtitude: $recent_bleats_longtitude{$time} </div><p>";
                        }
                        if ($recent_bleats_image{$time} && $recent_bleats_image{$time} ne '') {
                            print "<img src='$recent_bleats_image{$time}' class='img-thumbnail'> <p>";
                        }
                        print
                        "<form method='POST' action=''>
                        <input type='submit' value='View Replies' class='btn btn-success'>
                        <input type='hidden' name='result_detail_id' value='$recent_bleats_id{$time}'>
                        <input type='submit' value='Reply to Bleat' class='btn btn-success'>
                        <input type='hidden' name='new_bleat_replyto' value='$recent_bleats_id{$time}'>
                        <input type='hidden' name='new_bleat_replyto_username' value='$recent_bleats_username{$time}'>";
                        if ($recent_bleats_username{$time} eq $current_username) {
                            print "<input type='submit' name='delete_my_bleat' value='Delete Bleat' class='btn btn-success'>
                            <input type='hidden' name='delete_bleat_id' value='$recent_bleats_id{$time}'>";
                        }
                        print "<input type='hidden' name='login_username' value='$current_username'>
                            <input type='hidden' name='login_password' value='$current_password'>
                        </form></div></div><p>";
                        $count++;
                    }
                if ($flag == 1 && $count == 10) {
                    $start[$k] = $time;
                    print 
                        "<form>
                        <input type='submit' name='go_to_bleat_page' value='Next' class='btn btn-success'>
                        <input type='hidden' name='key_time' value=$start[$k]>
                        <input type='hidden' name='login_username' value='$current_username'>
                        <input type='hidden' name='login_password' value='$current_password'>
                        </form>
                        </div><p>";
                    $k++;
                    $flag = 0;
                    last;
                }
            }
        }           
    }
    if (defined param('result_detail_username')) {
        username_detail();
    }
    if (defined param('result_detail_id')) {
        bleat_replies();
    }
}