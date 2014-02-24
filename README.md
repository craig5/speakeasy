speakeasy
=========

Aggregate metrics locally before shipping them off to central metrics storage. Supports fetching data from server in real time.


Example
=======

	speakeasy -ms /var/tmp/metrics_socket \
		-cp 9839 \
		-pp 9840 \
		-e amf \
		-ea fabric=ela4\
		-ei 60 --verbose"
