const locc = window.location.origin;



function main(){
	let listOld = []
	let listNew = []

	fetch(`${locc}/notifications-api/`)
	.then(response =>  response.json())
	.then(data => {
		for (let i=0; i<data.lines.length; i++) {
			listNew.push(data.lines[i])
		}
	})

	for (let i=0; i<listNew.length; i++) {
		listOld.push(listNew[i])
		console.log(listOld);
	}


	// 

	// for (let i=0; i<list.length; i++) {
	// 	listOld.push(list[i])
	// }

	// return listOld

	// if (listOld.length < list.length) {
	// 	console.log('true');
	// }else{
	// 	console.log('false');
	// }
	// console.log(listOld);
}
// main()