 function openwin_project() {
            document.getElementById('new_project').style.display='block';
        }
        function closewin_project() {
            document.getElementById('new_project').style.display='none';
        }
        function closewin_project_editor() {
            document.getElementById('editor_project').style.display='none';
        }
        function delproject(obj) {
            var cell1 = obj.parentNode.parentNode.children[0];
            var ids = cell1.innerHTML;
            var data = {'id':ids};
            $.ajax({
                type:'GET',
                url:"{{url_for('delete_project')}}",
                data:data,
                dataType:'json',
                async:true
            })
        }
        function editor_project(obj) {
            document.getElementById('editor_project').style.display='block';
            var id_num = obj.parentNode.parentNode.children[0].innerHTML;
            var project_name = obj.parentNode.parentNode.children[1].innerHTML;
            var creator = obj.parentNode.parentNode.children[2].innerHTML;
            document.getElementsByName('num1')[0].value = id_num;
            document.getElementsByName('project_name1')[0].value = project_name;
            document.getElementsByName('creator1')[0].value = creator;
        }