import curses
import textwrap

import npyscreen.fmPopup
import npyscreen.wgmultiline
import pyperclip

import main
import securityGroupsGrid
import mainForm
import securityRulesForm


class ConfirmCancelPopup(npyscreen.fmPopup.ActionPopup):
    def on_ok(self):
        self.value = True

    def on_cancel(self):
        self.value = False

class displayPopup(npyscreen.fmPopup.Popup):
    def on_ok(self):
        self.editing = False
        self.value = True


def readString(form_color='STANDOUT'):

    F = ConfirmCancelPopup(name='', color=form_color)
    F.preserve_selected_widget = True
    tf = F.add(npyscreen.Textfield)
    tf.width = tf.width - 1
    tf.value = default_value
    F.edit()
    if F.value is True:
        return tf.value
    else:
        return None


def readAKSK(form_color='STANDOUT'):
    while True:
        F = ConfirmCancelPopup(name='New profile', color=form_color)
        F.preserve_selected_widget = True
        name = F.add(npyscreen.TitleText, name="NAME:")
        ak = F.add(npyscreen.TitleText, name="ACCESS KEY:")
        sk = F.add(npyscreen.TitleText, name="SECRET KEY:")
        region = F.add_widget(
            npyscreen.TitleCombo,
            name="REGION:",
            values="eu-west-2 eu-west-1".split(),
            value=0,
        )
        #ak.width = ak.width - 1
        F.edit()
        if F.value is True:
            if name.value != '' and ak.value != '' and sk.value != '':
                return {
                    name.value: {
                        'access_key': ak.value,
                        'secret-key': sk.value,
                        'region': region.values[region.value]
                    }
                }
            else:
                npyscreen.notify_confirm(
                    "Please check that you filled all fields.", "ERROR")
        else:
            return None


def editInstance(form, instance, form_color='STANDOUT'):
        status = instance[0]
        id = instance[2]
        name = instance[1]
        F = displayPopup(name=name + ' (' + id + ')', color=form_color)
        F.preserve_selected_widget = True
        def exit():
            form.current_grid.refresh()
            F.editing = False
        F.on_ok = exit
        # Buttons about VMs
        run_stop = F.add_widget(
            npyscreen.ButtonPress,
            name="RUN",
        )
        restart = F.add_widget(
            npyscreen.ButtonPress,
            name="RESTART",
        )
        force_stop = F.add_widget(
            npyscreen.ButtonPress,
            name="FORCE STOP",
        )
        terminate = F.add_widget(
            npyscreen.ButtonPress,
            name="TERMINATE",
        )
        copy_ip = F.add_widget(
            npyscreen.ButtonPress,
            name="COPY IP",
        )
        security = F.add_widget(
            npyscreen.ButtonPress,
            name="SECURITY",
        )
        #Now managing actions and wich buttons to hide or not.
        force_stop.hidden = (True if status == "stopped"
                             or status == "terminated" else False)
        restart.hidden = False if status == "running" else True
        security.hidden = True if status == "terminated" else False
        copy_ip.hidden = (True if status == "terminated" or status == "stopped"
                          else False)
        terminate.hidden = True if status == "terminated" else False
        if status == "running" or status == "stopped":
            run_stop.name = "RUN" if status == "stopped" else "STOP"
            run_stop.hidden = False
        else:
            run_stop.hidden = True
        if status == "terminated":
            security.hidden = True
        else:
            security.hidden = False
        run_stop.update()

        # Operations availables:
        def start_vm():
            main.GATEWAY.StartVms(VmIds=[id])
            exit()

        def terminate_vm():
            main.kill_threads()
            if npyscreen.notify_ok_cancel(
                    "Do you really want to terminate this vm:\nName: " + name +
                    "\nID: " + id,
                    "VM Termination",
            ):
                main.GATEWAY.DeleteVms(VmIds=[id])
            exit()

        def stop_vm():
            main.GATEWAY.StopVms(VmIds=[id])
            exit()

        def force_stop_vm():
            main.GATEWAY.StopVms(ForceStop=True, VmIds=[id])
            exit()

        def restart_vm():
            main.GATEWAY.RebootVms(VmIds=[id])
            exit()

        def sg():
            exit()
            main.kill_threads()
            main.VM = main.VMs[id]
            mainForm.CURRENT_GRID_CLASS = securityGroupsGrid.SecurityGroupsGridForOneInstance
            mainForm.MODE = 'SECURITY-VM'
            form.reload()


        def _copy_ip():
            pyperclip.copy(instance[5])
            exit()

        copy_ip.whenPressed = copy_ip
        run_stop.whenPressed = start_vm if status == "stopped" else stop_vm
        force_stop.whenPressed = force_stop_vm
        restart.whenPressed = restart_vm
        security.whenPressed = sg
        terminate.whenPressed = terminate_vm
        copy_ip.whenPressed = _copy_ip
        F.edit()

def editSecurityGroup(form, sg, form_color='STANDOUT'):
    name = sg[1]
    id = sg[0]
    main.SECURITY_GROUP = id
    F = displayPopup(name=name + ' (' + id + ')', color=form_color)
    F.preserve_selected_widget = True

    def exit():
        form.current_grid.refresh()
        F.editing = False

    F.on_ok = exit
    edit = F.add_widget(
        npyscreen.ButtonPress,
        name="EDIT",
    )

    def edit_cb():
        exit()
        form.parentApp.addForm(
            "SecurityRules",
            securityRulesForm.SecurityRulesForm,
            name="osc-cli-curses",
        )
        form.parentApp.switchForm("SecurityRules")

    delete = F.add_widget(
        npyscreen.ButtonPress,
        name="DELETE",
    )
    edit.whenPressed = edit_cb
    F.edit()

