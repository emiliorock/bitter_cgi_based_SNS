#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Session;

`echo "hi" | mutt -s "subject" "misty.hmx@gmail.com"`;

print "hi";