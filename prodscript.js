
window.addEventListener('load',function(){

    document.getElementById("table").addEventListener("click", function(e) {
    	if(e.target.className === "edit"){
    		var barcode = e.target.parentNode.id;
    		document.getElementById("editBox").style.display = "block";
    		document.editForm.action="/edit/" + barcode;
    		document.getElementById("editName").value = document.getElementById("name"+barcode).innerHTML;
    		document.getElementById("editPrice").value = document.getElementById("price"+barcode).innerHTML;
    		document.getElementById("editAv").value = document.getElementById("av"+barcode).innerHTML;
    		document.getElementById("editMinQ").value = document.getElementById("minQ"+barcode).innerHTML;
    		document.getElementById("editDesc").value = document.getElementById("desc"+barcode).innerHTML;
    	}

    	if(e.target.className === "editPerson"){
    		var name = e.target.parentNode.id;
    		document.getElementById("editBox").style.display = "block";
    		document.editForm.action="/edit/" + name;
    		//document.getElementById("editDebt").value = document.getElementById("debt"+name).innerHTML;
    		document.getElementById("editBalance").value = document.getElementById("Balance"+name).innerHTML;
    	}

    	if(e.target.className === "delete"){
    		var barcode = e.target.parentNode.id;
    		location.pathname = '/delete/'+barcode;
    	}

    	if(e.target.className === "deletePerson"){
    		var name = e.target.parentNode.id;
    		location.pathname = '/deletePerson/'+name;
    	}



		var col = e.target.parentNode;
		if(col.className === "collapsible"){
			var content = col.nextElementSibling;
			 if (content) {
	            if (content.style.display === "block") {
			      content.style.display = "none";
			    } else {
			      content.style.display = "block";
			    }
	        }
		}  
	});
});

function hasClass(elem, cls) {
    var str = " " + elem.className + " ";
    var testCls = " " + cls + " ";
    return(str.indexOf(testCls) != -1) ;
}

function nextByClass(node, cls) {
    while (node = node.nextSibling) {
		console.log(node, cls);
		console.log("ola");
        if (hasClass(node, cls)) {
            return node;
        }
    }
    return null;
}

function addItem() {
	//document.getElementById("create").setAttribute("onClick", "javascript: return createItem()");
	document.getElementById("createBox").style.display = "block";
}



function createItem(){

	var barcode = document.getElementById("barcode");
	if(isNaN(barcode.value) || barcode.value === ""){
		barcode.style.borderColor = "red";
		console.log("fail");
	} else {
		console.log("suc");
		location.pathname = '/new';

	}
	return false
}

function addPerson() {
	//document.getElementById("create").setAttribute("onClick", "javascript: return createItem()");
	document.getElementById("createBox").style.display = "block";
}
