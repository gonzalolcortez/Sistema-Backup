from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Tecnico

tecnicos_bp = Blueprint('tecnicos', __name__)


@tecnicos_bp.route('/')
@login_required
def index():
    tecnicos = Tecnico.query.order_by(Tecnico.nombre).all()
    return render_template('tecnicos/index.html', tecnicos=tecnicos)


@tecnicos_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        es_tercerizado = request.form.get('es_tercerizado') == '1'
        tecnico = Tecnico(
            nombre=request.form['nombre'].strip(),
            es_tercerizado=es_tercerizado,
            empresa_tercerizado=request.form.get('empresa_tercerizado', '').strip() if es_tercerizado else None,
        )
        db.session.add(tecnico)
        db.session.commit()
        flash('Técnico creado correctamente.', 'success')
        return redirect(url_for('tecnicos.index'))
    return render_template('tecnicos/form.html', tecnico=None, titulo='Nuevo Técnico')


@tecnicos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    tecnico = Tecnico.query.get_or_404(id)
    if request.method == 'POST':
        es_tercerizado = request.form.get('es_tercerizado') == '1'
        tecnico.nombre = request.form['nombre'].strip()
        tecnico.es_tercerizado = es_tercerizado
        tecnico.empresa_tercerizado = request.form.get('empresa_tercerizado', '').strip() if es_tercerizado else None
        db.session.commit()
        flash('Técnico actualizado.', 'success')
        return redirect(url_for('tecnicos.index'))
    return render_template('tecnicos/form.html', tecnico=tecnico, titulo='Editar Técnico')


@tecnicos_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    tecnico = Tecnico.query.get_or_404(id)
    tecnico.activo = not tecnico.activo
    db.session.commit()
    estado = 'activado' if tecnico.activo else 'desactivado'
    flash(f'Técnico {estado}.', 'success')
    return redirect(url_for('tecnicos.index'))
