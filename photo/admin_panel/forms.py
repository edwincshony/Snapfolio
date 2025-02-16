class PortfolioApprovalForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['is_approved']