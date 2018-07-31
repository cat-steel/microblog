 function openwin() {
            document.getElementById('add_testcase').style.display='block';
        }
        function closewin() {
            document.getElementById('add_testcase').style.display='none';
        }
        function closewin_editor() {
            document.getElementById('editor_testcase').style.display='none';
        }
        function delcase(obj) {
            var cell1 = obj.parentNode.parentNode.children[1];
            var ids = cell1.innerHTML;
            var data = {'id':ids};
            $.ajax({
                type:'GET',
                url:"{{url_for('delete_case')}}",
                data:data,
                dataType:'json',
                async:true
            })
        }
        function editor(obj) {
            document.getElementById('editor_testcase').style.display='block';
            var id_num = obj.parentNode.parentNode.children[1].innerHTML;
            var case_name = obj.parentNode.parentNode.children[2].innerHTML;
            var IP = obj.parentNode.parentNode.children[3].innerHTML;
            var ways = obj.parentNode.parentNode.children[4].innerHTML;
            var request_method = obj.parentNode.parentNode.children[5].innerHTML;
            var data_i = obj.parentNode.parentNode.children[6].innerHTML;
            var data = obj.parentNode.parentNode.children[7].innerHTML;
            var check = obj.parentNode.parentNode.children[8].innerHTML;
            var is_base = obj.parentNode.parentNode.children[9].innerHTML;
            document.getElementsByName('num1')[0].value = id_num;
            document.getElementsByName('names1')[0].value = case_name;
            document.getElementsByName('server1')[0].value = IP;
            document.getElementsByName('way1')[0].value = ways;
            document.getElementsByName('request_method1')[0].value = request_method;
            document.getElementsByName('data_i1')[0].value = data_i;
            document.getElementsByName('data1')[0].value = data;
            document.getElementsByName('check1')[0].value = check;
            document.getElementsByName('is_base1')[0].value = is_base;
        }