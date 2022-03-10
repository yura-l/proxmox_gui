// const alertBox = document.getElementById('alert-box')
// const form = document.getElementsByName('form-card-id')
//
// // forEach(
// //    // elem.addEventListener("input", function() {
// //       form.addEventListener('submit', e=>{
// //       e.preventDefault()
// //       console.log(window.event.target.id);
// //       let  uuid = document.getElementsByName('Numd');
// //       console.log(uuid[0].value)
// // //
// //
// //         //this function does stuff
// //     });
// // );
//
// form.forEach(function(elem) {
//     elem.addEventListener('submit', e=>{
//           e.preventDefault()
//           // console.log(elem.getAttribute('method'))
//             // let  uuid = document.getElementsByName('Numd');
//            let formData = new FormData(e.target);
//            let formProps = Object.fromEntries(formData)
//            let uuid = formProps['Numd']
//             $.ajax({
//                   type: elem.getAttribute('method'),
//                   url: {% url 'stop' %},       //elem.getAttribute('action'),
//                   data: {uuid : uuid },
//
//                   success: function (data) {
//                         console.log('Submission was successful.');
//                         console.log(data);
//                   },
//                   error: function (data) {
//                         console.log('An error occurred.');
//                         console.log(data);
//                   },
//             });
//     });
// });
//
// //
// //
//
// // const description = document.getElementById('id_description')
// // const stop = document.getElementById('stop1')
// //  console.log(stop)
// // console.log('------------------')
// // // const csrf = document.getElementsByName('csrfmiddlewaretoken')
// // console.log(name)
// // //
// // const url = ""
// // //
// // const handleAlerts = (type, text) => {
// //     alertBox.innerHTML = <div class="alert alert-${type}" role="alert">
// //         ${text}                    </div>
// // }
//
//
//
//
// //
// // $("#stop1").click(function() {
// //    console.log("btn click");
// //    x =  document.getElementsByName('stop1')
// //    console.log(x);
// // });
//
//     // [ 'name', 'age' ]
// //
//
//
//
// // //
// //      const fd = new FormData()
// //         fd.append('csrfmiddlewaretoken', csrf[0].value)
// //         fd.append('Numd', name.value)
// // //     fd.append('description', description.value)
// // //     fd.append('image', image.files[0])
// // //
// //         console.log(name)
// // })
// //
// // //     $.ajax({
// // //         type: 'POST',
// // //         url: url,
// // //         enctype: 'multipart/form-data',
// // //         data: fd,
// // //         success: function(response){
// // //             console.log(response)
// // //             const sText = `successfully saved ${response.name}`
// // //             handleAlerts('success', sText)
// // //             setTimeout(()=>{
// // //                 alertBox.innerHTML = ""
// // //                 imgBox.innerHTML = ""
// // //                 name.value = ""
// // //                 description.value = ""
// // //                 image.value = ""
// // //             }, 3000)
// // //         },
// // //         error: function(error){
// // //             console.log(error)
// // //             handleAlerts('danger', 'ups..something went wrong')
// // //         },
// // //         cache: false,
// // //         contentType: false,
// // //         processData: false,
//
// // //
// // // console.log(form)