var $ = jQuery.noConflict();

function abrir_modal_creacion(url) {
    $('#creacion').load(url, function () {
        $(this).modal('show')
    });
}
function abrir_modal_edicion(url) {
    $('#edicion').load(url, function () {
        $(this).modal('show')
    });
}

function cerrar_modal_creacion() {
    $('#creacion').modal('hide');
}

function cerrar_modal_edicion() {
    $('#edicion').modal('hide');
}

function eliminarpaciente(id){
    //console.log(id)           
    Swal.fire({
        title: 'Estas seguro?',
        text: "Se borrará de forma permanente!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonText: 'Cancelar',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si eliminar'
        }).then(function(result) {
            if (result.isConfirmed) {
                window.location.href= "/eliminar_paciente/"+id+"/"
              
                }
            })
        }
function eliminardoctor(id){
        //console.log(id)           
        Swal.fire({
            title: 'Estas seguro?',
            text: "Se borrará de forma permanente!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonText: 'Cancelar',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si eliminar'
            }).then(function(result) {
                if (result.isConfirmed) {
                    window.location.href= "/eliminar_doctor/"+id+"/"
                    }
                })
            }

function eliminarcita(id) {
        //console.log(id)           
        Swal.fire({
            title: 'Estas seguro?',
            text: "Se borrará de forma permanente!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonText: 'Cancelar',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si eliminar'
            }).then(function (result) {
                if (result.isConfirmed) {
                    window.location.href = "/eliminar_cita/" + id + "/"
                    }
                })
            }

function eliminartratamiento(id){
        //console.log(id)           
        Swal.fire({
            title: 'Estas seguro?',
            text: "Se borrará de forma permanente!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonText: 'Cancelar',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si eliminar'
            }).then(function(result) {
                if (result.isConfirmed) {
                    window.location.href= "/eliminar_tratamiento/"+id+"/"
                      
                    }
                })
     
            }

$('.btn-exit-system').on('click', function(e){
    e.preventDefault();
    Swal.fire({
        title: 'Esta seguro?',
        text: 'quiere salir de la aplicacion web ',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonText: 'Cancelar',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Salir '
        }).then((result) => {
            if (result.value) {
                window.location.href= "/logout/";
                }
            });
    });


function eliminarusuario(id){
    //console.log(id)           
    Swal.fire({
        title: 'Estas seguro?',
        text: "Se borrará de forma permanente!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonText: 'Cancelar',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si eliminar'
        }).then(function(result) {
            if (result.isConfirmed) {
                window.location.href= "/eliminar_cita/"+id+"/"
                }
            })
        }

