 function openwin_module() {
            document.getElementById('new_module').style.display='block';
        }
        function closewin_module() {
            document.getElementById('new_module').style.display='none';
        }
        function closewin_modul_editor() {
            document.getElementById('editor_module').style.display='none';
        }
        function delmudole(obj) {
            var cell1 = obj.parentNode.parentNode.children[0];
            var ids = cell1.innerHTML;
            var data = {'id':ids};
            $.ajax({
                type:'GET',
                url:"{{url_for('delete_module')}}",
                data:data,
                dataType:'json',
                async:true
            })
        }
        function editor_module(obj) {
            document.getElementById('editor_module').style.display='block';
            var id_num = obj.parentNode.parentNode.children[0].innerHTML;
            var module_name = obj.parentNode.parentNode.children[1].innerHTML;
            var creator = obj.parentNode.parentNode.children[2].innerHTML;
            document.getElementsByName('num1')[0].value = id_num;
            document.getElementsByName('module_name1')[0].value = module_name;
            document.getElementsByName('creator1')[0].value = creator;
        }