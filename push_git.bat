:start

@set d="auto" 
@set t=%date%%time%
@set /p d=git commit: 

@ git add . &&git commit -m "%t% %d%" && git push 
@rem pause
@echo -----------------------------------------------------------------
@goto start
